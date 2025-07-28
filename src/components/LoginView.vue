<script>
import { mapState, mapActions } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  emits: ['login-success'],

  data() {
    return {
      name: '',
    }
  },
  computed: {
    ...mapState(useSettingsStore, [
      'fontSize',
      'buttonColor',
      'buttonHoverColor',
      'resultColor',
      'resultHoverColor',
      'blackFont',
      'whiteFont',
    ]),
  },
  methods: {
    ...mapActions(useSettingsStore, [
      'increaseFontSize',
      'decreaseFontSize',
      'resetFontSize',
      'setTheme',
      'setData',
    ]),

    executePython() {
      this.isLoading = true
      this.pythonResult = null

      fetch('http://localhost:3001/run-python-file')
        .then((response) => response.json())
        .then((data) => {
          this.pythonResult = data
        })
        .catch((error) => {
          console.error('Error:', error)
          this.pythonResult = { message: 'Error fetching results.' }
        })
        .finally(() => {
          this.isLoading = false
        })
    },

    submitName() {
      if (this.name.trim()) {
        this.$emit('login-success', this.name.trim())
      } else {
        alert('お名前を入力してください')
      }
    },
    goToResults() {
      this.$emit('show-results')
    },
    goToLogin() {
      this.$emit('show-login')
    },
    dataSetter(_data) {
      this.data = _data
    },
  },
}
</script>

<template>
  <div class="login-container">
    <form @submit.prevent="submitName" :style="{ 'font-size': fontSize + 'px' }">
      <label>お名前を入力してください : </label><br />
      <input
        v-model="name"
        placeholder="input name"
        maxlength="15"
        :style="{ 'font-size': fontSize + 'px' }"
      />
      <br />
      <button type="button" class="submit" @click="submitName">アンケート開始</button>
      <button
        type="button"
        class="result-button"
        @click="(executePython(setData(data)), goToResults())"
      >
        結果を見る
      </button>
      <br />
      <div class="font-button-group">
        <button type="button" class="font-size-changer" @click="increaseFontSize">大きく</button>
        <button type="button" class="font-size-changer" @click="decreaseFontSize">小さく</button>
        <button type="button" class="font-size-changer" @click="resetFontSize">初期化</button>
      </div>
      <label :style="{ 'font-size': fontSize - 3 + 'px' }">文字の大きさ : {{ fontSize }}</label>
      <div class="font-button-group" :style="({ gap: 2 + 'em' }, { 'margin-top': 1 + 'em' })">
        <button type="button" class="color-changer" @click="setTheme('light')">色モード</button>
        <button type="button" class="bwcolor-changer" @click="setTheme('dark')">白黒モード</button>
      </div>
      <br />
    </form>
  </div>
</template>

<style scoped>
/* 스타일은 변경 없습니다 */
.login-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}
.font-button-group {
  display: flex;
  gap: 0.4em;
  margin-top: 3em;
  margin-bottom: 0.3em;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.font-size-changer {
  flex: 1;
  padding: 0.6em 0;
  background: v-bind(buttonColor);
  color: #fff;
  border: none;
  border-radius: 0.25em;
  cursor: pointer;
  font-size: var(--font-size);
}

.font-size-changer:hover {
  background: v-bind(buttonHoverColor);
}

.submit {
  font-size: var(--font-size);
  background: v-bind(buttonColor);
  margin-top: 0.5em;
}
.submit:hover {
  font-size: var(--font-size);
  background: v-bind(buttonHoverColor);
}

.result-button {
  background: v-bind(resultColor);
  margin-top: 0.5em;
  color: v-bind(whiteFont);
  font-size: var(--font-size);
}
.result-button:hover {
  background: v-bind(resultHoverColor);
  font-size: var(--font-size);
}

.color-changer {
  flex: 1;
  padding: 0.6em 0;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 0.25em;
  cursor: pointer;
  font-size: var(--font-size);
}

.color-changer:hover {
  font-size: var(--font-size);
  background: #369870;
}

.bwcolor-changer {
  flex: 1;
  padding: 0.6em 0;
  background: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 0.25em;
  cursor: pointer;
  font-size: var(--font-size);
}
.bwcolor-changer:hover {
  font-size: var(--font-size);
  background: #7a7a7a;
}
button {
  width: 100%;
  padding: 10px 0;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: #369870;
}
</style>
