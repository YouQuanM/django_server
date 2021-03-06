// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Toast from './components/toast/index.js'
import './components/toast/toast.css';
import Vuex from 'vuex'
import store from './store/index.js'
// import uploader from 'vue-easy-uploader'
Vue.use(Vuex)

// let store = new Vuex.Store({})
// Vue.use(store)
Vue.config.productionTip = false

Vue.use(Toast);


new Vue({
  el: '#app',
  router,
  store,//使用store
  components: {
    App,
  },
  template: '<App/>'
})
