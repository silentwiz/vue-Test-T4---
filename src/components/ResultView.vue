<script>
import { mapState } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  data() {
    return {
      pythonResult: null,
      isLoading: false,
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
    goToLogin() {
      this.$emit('show-login')
    },
  },
}
</script>

<template>
  <div class="result-container">
    <h2>分析結果</h2>
    <button class="submit" @click="executePython" :disabled="isLoading">
      {{ isLoading ? '分析中...' : 'Python スクリプト実行' }}
    </button>
    <button type="button" class="result-button" @click="goToLogin">戻る</button>

    <div v-if="pythonResult && pythonResult.message" class="result-display">
      <p>
        <b>結果:</b><br />
        python status : {{ pythonResult.message }} <br />
        Time: {{ pythonResult.nowTime }} <br />
        Random Number: {{ pythonResult.randomNumber }}
      </p>

      <div v-if="pythonResult.plotImage" class="plot-image">
        <img :src="'data:image/png;base64,' + pythonResult.plotImage" alt="Matplotlib Plot" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.result-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
}
.plot-image img {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
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

.submit {
  font-size: var(--font-size);
  background: v-bind(buttonColor);
  margin-top: 0.5em;
}
.submit:hover {
  font-size: var(--font-size);
  background: v-bind(buttonHoverColor);
}
</style>
