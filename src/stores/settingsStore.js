import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  // state:
  state: () => ({
    fontSize: 16,
    buttonColor: '#5AAE61',
    buttonHoverColor: '#1B7837',
    resultColor: '#4393C3',
    resultHoverColor: '#2166AC',
    blackFont: '#000000',
    whiteFont: '#ffffff',
    data: '',
    bgColor: '#ffffff',
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
        this.resultColor = '#777777'
        this.resultHoverColor = '#131313ff'
        this.bgColor = '#777777'
      } else {
        // default mode
        this.buttonColor = '#5AAE61'
        this.buttonHoverColor = '#1B7837'
        this.resultColor = '#4393C3'
        this.resultHoverColor = '#2166AC'
        this.bgColor = '#ffffff'
      }
    },
    setData(data) {
      this.data = data
    },
  },
})
