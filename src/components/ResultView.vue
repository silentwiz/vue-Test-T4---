<script>
import { mapState } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  data() {
    return {
      pythonResult: null,
      isLoading: true,
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
      'data',
    ]),
  },
  mounted() {
    this.executePython()
  },

  watch: {
    // bgColor 값이 변경될 때마다 이 함수가 실행됩니다.
    bgColor(newColor) {
      document.body.style.backgroundColor = newColor
    },
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
    <button type="button" class="result-button" @click="goToLogin">戻る</button>

    <div v-if="pythonResult && pythonResult.message" class="result-display">
      <p>
        <b>結果:</b><br />
        python status : {{ pythonResult.message }} <br />
        Time: {{ pythonResult.nowTime }} <br />
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
