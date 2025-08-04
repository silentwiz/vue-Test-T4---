<template>
  <div class="result-view" :style="{ 'font-size': fontSize + 'px' }">
    <h1>アンケート結果</h1>
    <div class="button-group">
      <button class="submit" @click="fetchGraph">グラフ再生成</button>
      <button type="button" class="submit" @click="goToLogin">戻る</button>
    </div>
    <div v-if="loading" class="loading-message">作成中。。。</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="plotImage" class="graph-container" :class="{ fullscreen: isFullscreen }">
      <img
        :src="`data:image/png;base64,${plotImage}`"
        alt="Survey Results Graph"
        @click="toggleFullscreen"
      />
    </div>
    <div v-if="message" class="info-message">{{ message }}</div>
  </div>
</template>

<script>
import { mapState } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  name: 'ResultView',
  data() {
    return {
      plotImage: null,
      loading: false,
      error: null,
      message: null,
      isFullscreen: false,
    }
  },
  mounted() {
    this.fetchGraph()
    document.addEventListener('keydown', this.handleKeydown)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleKeydown)
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
      'bgColor',
    ]),
  },
  methods: {
    async fetchGraph() {
      this.loading = true
      this.error = null
      this.plotImage = null
      this.message = null

      try {
        const response = await fetch('/api/results')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()

        if (data.plotImage) {
          this.plotImage = data.plotImage
        } else if (data.error) {
          this.error = `グラフ生成失敗: ${data.error}`
        } else if (data.message) {
          this.message = data.message
        }
      } catch (e) {
        this.error = 'Python読み込み失敗'
        console.error(e)
      } finally {
        this.loading = false
      }
    },
    goToLogin() {
      this.$emit('show-login')
    },
    toggleFullscreen() {
      this.isFullscreen = !this.isFullscreen
    },
    handleKeydown(event) {
      if (event.key === 'Escape' && this.isFullscreen) {
        this.isFullscreen = false
      }
    },
  },
}
</script>

<style scoped>
button {
  width: 30%;
  padding: 10px 0;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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

.result-view {
  background-color: #fff;
  padding: 20px;
  text-align: center;
  max-width: 100%;
  margin: 0 auto;
  min-height: 100vh;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.button-group button {
  width: auto;
  padding: 12px 24px;
  font-size: var(--font-size);
}

.graph-container {
  margin-top: 20px;
  width: 100%;
  overflow-x: auto;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  background: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.graph-container img {
  width: auto;
  height: auto;
  max-width: 100%;
  min-width: 800px;
  cursor: pointer;
  border-radius: 8px;
}

.graph-container.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.95);
  padding: 20px;
  border-radius: 0;
  overflow: auto;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

.graph-container.fullscreen img {
  width: auto;
  height: auto;
  max-width: none;
  max-height: none;
  min-width: none;
  cursor: zoom-out;
  transform: none;
  object-fit: contain;
  max-width: calc(100vw - 40px);
}

.graph-container.fullscreen img:hover {
  transform: none;
}

.graph-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.graph-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.graph-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.graph-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
    align-items: center;
  }

  .button-group button {
    width: 200px;
    margin: 5px 0;
  }

  .graph-container img {
    min-width: 100%;
  }

  .graph-container.fullscreen {
    padding: 20px;
  }
}

.loading-message,
.error-message,
.info-message {
  margin-top: 20px;
  font-size: 1.2em;
  padding: 20px;
  border-radius: 8px;
}

.loading-message {
  background: #e3f2fd;
  color: #1976d2;
}

.error-message {
  background: #ffebee;
  color: #d32f2f;
}

.info-message {
  background: #f3e5f5;
  color: #7b1fa2;
}
</style>
