<template>
  <div id="app">
    <x-header :left-options="{showBack: false}">liangzhi<button @click="login_minepage" slot="right">{{ login_text }}</button></x-header>
    <router-view/>
    <tabbar style="position: fixed">
      <tabbar-item select>
        <span slot="label" @click="goToSomewhere('/index')">index</span>
      </tabbar-item>
      <tabbar-item>
        <span slot="label" @click="goToSomewhere('/marticle')">article</span>
      </tabbar-item>
      <tabbar-item>
        <span slot="label">test</span>
      </tabbar-item>
      <tabbar-item>
        <span slot="label">test</span>
      </tabbar-item>
    </tabbar>
    <toast v-model="showSuccess" type="text" text="success"></toast>
    <popup v-model="loginVisible" height="100%">
      <div class="before_login">
        <popup-header title="登录"></popup-header>
        <group label-width="4.5em" label-margin-right="2em" label-align="right">
          <x-input label="用户名" placeholder="请输入用户名" v-model="login_username"></x-input>
          <x-input label="密码" placeholder="请输入密码" type="password" v-model="login_password"></x-input>
          <x-button type="primary" size="large" @click.native="logIn">登录</x-button>
          <x-button @click.native="loginVisible = false" size="large">取消</x-button>
        </group>
      </div>
    </popup>
    <popup v-model="personalCenter" position="right">
      <div style="width:200px;">

      </div>
    </popup>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from './define.js'
  let _ = require('lodash');
  import qs from 'qs';
  import { XButton,Drawer,XHeader,Popup,Group,PopupHeader,Tabbar,TabbarItem,Toast } from 'vux'
  import XImg from "../node_modules/vux/src/components/x-img/index.vue";
  import XInput from "../node_modules/vux/src/components/x-input/index.vue";
export default {
  components: {
    XInput,
    XImg,
    XButton,
    Drawer,
    XHeader,
    Popup,
    Group,
    PopupHeader,
    Tabbar,
    TabbarItem,
    Toast
  },
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
body{
  margin: 0;
  padding: 0;
}
</style>
