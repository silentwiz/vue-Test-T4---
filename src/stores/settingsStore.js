import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  // state:
  state: () => ({
    fontSize: 16,
    buttonColor: '#42b983',
    buttonHoverColor: '#369870',
    resultColor: '#5c6ac4',
    resultHoverColor: '#4a55a0',
    blackFont: '#000000',
    whiteFont: '#fff',
  }),

  // actions:
  actions: {
    increaseFontSize() {
      this.fontSize += 2
    },
    decreaseFontSize() {
      this.fontSize -= 2
    },
    resetFontSize() {
      this.fontSize = 16
    },
    setTheme(themeName) {
      this.theme = themeName
      if (themeName === 'dark') {
        // dark mode
        this.buttonColor = '#1a1a1a'
        this.buttonHoverColor = '#7a7a7a'
        this.resultColor = '#b9b9b9ff'
        this.resultHoverColor = '#555555'
      } else {
        // default mode
        this.buttonColor = '#42b983'
        this.buttonHoverColor = '#369870'
        this.resultColor = '#5c6ac4'
        this.resultHoverColor = '#4a55a0'
      }
    },
  },
})
