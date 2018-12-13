<template>
  <div class="logUp">
    <div class="logUp-title">
      用户注册
    </div>
    <div class="logUp-form">
      <input class="logUp-form-username" placeholder="请输入用户名">
      <input class="logUp-form-password1" placeholder="请输入密码">
      <input class="logUp-form-password2" placeholder="请确认密码">
      <input class="logUp-form-email" placeholder="请输入邮箱">
    </div>
    <div class="logUp-btnGroup">
      <div class="logUp-submit"></div>
      <div class="logUp-cancel"></div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'writeArticle',
  data () {
    return {
      article_title: '',
      article_body: ''
    }
  },
  mounted: function () {

  },
  methods: {

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .logUp-title { font-family: PingFangSC-Medium;  font-size: 38px;  color: rgba(85,85,85,1.00);  text-align: center;  }

  .logUp-form { width: 606px; margin: 0 auto;}

  .logUp-form input { width: 606px; height: 72px; margin: 0 auto; font-family: PingFangSC-Regular;  font-size: 32px;  color: #999999;  letter-spacing: 0; }
</style>
