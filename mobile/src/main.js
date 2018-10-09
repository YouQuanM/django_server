// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import qs from 'qs'

Vue.config.productionTip = false
import { XButton,Toast } from 'vux'

new Vue({
  el: '#app',
  router,
  components: {
    App,
    XButton,
    Toast
  },
  template: '<App/>'
})
