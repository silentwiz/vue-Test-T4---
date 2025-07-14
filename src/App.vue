<script>
import LoginView from './components/LoginView.vue'
import SurveyView from './components/SurveyView.vue'
import ResultView from './components/ResultView.vue'

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
  </div>
</template>

<style>
/* 전역 스타일은 여기에 남겨두거나 main.css 파일로 옮길 수 있습니다. */
body {
  background-color: #f4f4f4;
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: 0;
}
</style>
