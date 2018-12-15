<template>
  <div id="app">
    <div class="app-content">
      <router-view/>
    </div>
    <div class="app-footer" v-if="isShow">
      <div class="app-footer-item" @click="goToSomewhere('/index')">首页</div>
      <div class="app-footer-item" @click="goToSomewhere('/marticle')">文章</div>
      <div class="app-footer-item" @click="goToSomewhere('/mine')">我的</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {

    }
  },
  computed:{
     isShow(){
       return this.$store.getters.isShow;
     }
  },
  watch: {
    $route(to,from){ //跳转组件页面后，监听路由参数中对应的当前页面以及上一个页面
        console.log(to);
        if(to.name=='writeArticle' || to.name=='articleDetail'){ // to.name来获取当前所显示的页面，从而控制该显示或隐藏footerBar组件
         this.$store.dispatch('hideFooter') // 利用派发全局state.showFooter的值来控制
        } else{
         this.$store.dispatch('showFooter')
        }
    }
  },
  created() {
  },
  methods: {
    goToSomewhere (navi) {
      let that = this;
      that.$router.replace(navi)
    }
  }
}
</script>

<style>
  html { font-size: 20px; }

  html,body{ margin: 0;  padding: 0; height: 100%; }

  * { max-height: 99999px;}

  #app { display: flex; flex-direction: column; align-items: stretch; height: 100%;}

  .app-content { flex: 1 0 auto; width: 100%;}

  .app-footer { position: fixed; bottom: 0; flex: 0 0 auto; display: flex; flex-direction: row; width: 100%; height: 100px; background: #FFF; border-top: 1px solid #999999; }

  .app-footer-item { width: 250px; line-height: 100px; text-align: center;}

</style>
