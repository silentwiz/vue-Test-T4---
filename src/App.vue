<script>
import LoginView from './components/LoginView.vue'
import SurveyView from './components/SurveyView.vue'
import ResultView from './components/ResultView.vue'

import { mapState } from 'pinia'
import { useSettingsStore } from '@/stores/settingsStore'

export default {
  components: {
    LoginView,
    SurveyView,
    ResultView,
  },
  data() {
    return {
      currentView: 'LoginView',
      userName: '',
    }
  },
  computed: {
    ...mapState(useSettingsStore, ['bgColor']),
  },
  mounted() {
    document.body.style.backgroundColor = this.bgColor
  },
  watch: {
    bgColor(newColor) {
      document.body.style.backgroundColor = newColor
    },
  },

  methods: {
    handleLogin(name) {
      this.userName = name
      this.currentView = 'SurveyView'
    },
    showResults() {
      this.currentView = 'ResultView'
    },
    showLogin() {
      this.currentView = 'LoginView'
    },
  },
}
</script>

<template>
  <div>
    <component
      :is="currentView"
      :user-name="userName"
      @login-success="handleLogin"
      @show-results="showResults"
      @show-login="showLogin"
    ></component>

    <label> {{ bgColor }}</label>
  </div>
</template>

<style>
body {
  width: auto;
  background-color: v-bind(bgColor);
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: 0;
}
</style>
