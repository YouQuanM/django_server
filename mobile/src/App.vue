<template>
  <div id="app">
    <div class="app-content">
      <router-view/>
    </div>
    <div class="app-footer">
      <div class="app-footer-item" @click="goToSomewhere('/index')">index</div>
      <div class="app-footer-item" @click="goToSomewhere('/marticle')">article</div>
      <div class="app-footer-item" @click="goToSomewhere('/mine')">mineSpace</div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from './define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'App',
  data () {
    return {
      login_username: '',
      login_password: '',
      login_text: '登录',
      dialogFormVisible: false,
      logup_from: {
        username: '',
        password: '',
        email: ''
      },
      logInFlag: 'block',
      logSuccessFlag: 'none',
      form_login: {
        username: '',
        password: ''
      },
      routerFlag: 'block',
      loginAreaFlag: 'none',
      selected: 'index',
      loginVisible: false,
      logMineFlag: 'log',
      showSuccess: false,
      personalCenter: false
    }
  },
  created() {
    this.getUserInfo();
  },
  methods: {
    getUserInfo(){
      let that = this;
      let article_user = sessionStorage.getItem("username");
      if (article_user){
        that.login_text = article_user;
        that.logInFlag = 'none';
        that.logSuccessFlag = 'block';
        that.logMineFlag = 'mine';
      }else {
        that.login_text = '登录';
        that.logInFlag = 'block';
        that.logSuccessFlag = 'none';
      }
    },
    toLogUp () {
      let that = this;
      that.loginVisible = false;
      that.$router.push({ path: '/logUp'});//跳转注册页面
    },
    logUp () {
      let that = this;
      let data = {
        username: that.logup_from.username,
        password: that.logup_from.password,
        email: that.logup_from.email
      };
      axios.post(AJAXURL + 'log_up',
        qs.stringify(data),
        {headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      }).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {
          console.log(res);
          that.$message.success('注册成功');
          that.dialogFormVisible = false;
        } else {
          that.$message.error('注册失败,'+response.msg);
          console.log(response['msg'])
        }
      })
    },
    logIn () {
      let that = this;
      let data = {
          username: that.login_username,
          password: that.login_password,
        };
      axios.post(AJAXURL + 'log_in',
        qs.stringify(data),
        {headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      }).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {
          that.login_username = '';
          that.login_password = '';
          that.loginVisible = false;
          that.logMineFlag = 'mine';
          that.showSuccess = true;
          that.login_text = response.username;
          sessionStorage.setItem("username", response.username);
          sessionStorage.setItem("userid", response.userid);
        } else {
          that.$message.error(response.msg);
        }
      })
    },
    logOut () {
      let that = this;
      axios.get(AJAXURL + 'log_out',{}).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {
          that.$message.info('登出');
          sessionStorage.removeItem('username');
          sessionStorage.removeItem('userid');
          that.login_text = '登录';
          that.logInFlag = 'block';
          that.logSuccessFlag = 'none';
          let path = that.$route.path;
          if (path == '/userpage'){
            that.$router.push('/#');
          }
        } else {
          that.$message.error(response.msg);
        }
      })
    },
    login_minepage () {
      let that = this;
      if (that.logMineFlag === 'log'){
        that.loginVisible = true;
      }else if (that.logMineFlag === 'mine') {
        //router到我的主页
        that.personalCenter = true;
      }
    },
    goToSomewhere (navi) {
      let that = this;
      that.$router.push(navi)
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
