<template>
  <div class="result-view">
    <h1>アンケート結果</h1>
    <button @click="fetchGraph">グラフ再生成</button>
    <div v-if="loading" class="loading-message">作成中。。。</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="plotImage" class="graph-container">
      <img :src="`data:image/png;base64,${plotImage}`" alt="Survey Results Graph" />
    </div>
    <div v-if="message" class="info-message">{{ message }}</div>
  </div>
</template>

<script>
export default {
  name: 'ResultView',
  data() {
    return {
      plotImage: null,
      loading: false,
      error: null,
      message: null, // For messages like 'No one has answered yet'
    }
  },
  mounted() {
    this.fetchGraph()
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
  },
}
</script>

<style scoped>
.result-view {
  padding: 20px;
  text-align: center;
}
.graph-container {
  margin-top: 20px;
  max-width: 100%;
  overflow-x: auto;
}
.graph-container img {
  max-width: none; /* Let the container handle scrolling */
  height: auto;
}
.loading-message,
.error-message,
.info-message {
  margin-top: 20px;
  font-size: 1.2em;
}
.error-message {
  color: red;
}
.info-message {
  color: grey;
}
</style>
