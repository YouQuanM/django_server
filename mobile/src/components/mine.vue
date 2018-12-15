<template>
  <div class="mine">
    <div class="mine-main" v-if="mine_flag">
      <div class="mine-header">
        <div class="header-default" @click="showLogIn()" v-if="!logIn_flag">
          点击登录
        </div>
        <div class="header-userinfo" v-if="logIn_flag">
          <div class="header-name">{{ user_name }}</div>
          <div class="header-email">{{ user_email }}</div>
        </div>
      </div>
      <div class="mine-content" v-if="logIn_flag">
        <div class="logout-btn" @click="logOut()">退出登录</div>
      </div>
    </div>
    <div class="mine-log" v-if="log_flag">
      <div class="log-img">
        {{ log_img_text }}
      </div>
      <div class="log-form" v-if="log_form_flag">
        <div class="log-form-item">
          <input type="text" v-model="login_username" placeholder="请输入用户名">
        </div>
        <div class="log-form-item">
          <input type="password" v-model="login_password" placeholder="请输入密码">
        </div>
        <div class="log-btn" @click="logIn()">登 录</div>
        <div class="cancel-btn" @click="cancel()">取 消</div>
        <div class="register-btn" @click="showLogUp()">注 册</div>
      </div>
      <div class="register-form" v-if="register_form_flag">
        <div class="register-form-item">
          <input type="text" v-model="register_username" placeholder="请输入用户名" @blur="checkName()">
          <p v-show="checkname_flag">用户名不能为空</p>
        </div>
        <div class="register-form-item">
          <input type="password" v-model="register_password" placeholder="请输入密码" @blur="checkPassword()">
          <p v-show="checkpassword_flag">密码至少为6位</p>
        </div>
        <div class="register-form-item">
          <input type="password" v-model="register_password_sure" @input="checkSurePassword()" placeholder="请确认密码">
          <p v-show="checkpassword_sure_flag">确认密码不正确</p>
        </div>
        <div class="register-form-item">
          <input type="email" v-model="register_email" placeholder="请输入邮箱" @blur="checkEmail()">
          <p v-show="checkemail_flag">邮箱格式不正确</p>
        </div>
        <div class="log-btn" @click="logUp()">注 册</div>
        <div class="cancel-btn" @click="cancel()">取 消</div>
        <div class="register-btn" @click="showLogIn()">返 回 登 录</div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'mine',
  data () {
    return {
//      flag
      logIn_flag: true,
      mine_flag: true,
      log_flag: false,
      log_form_flag: true,
      register_form_flag: false,
      checkname_flag: false,
      checkpassword_flag: false,
      checkpassword_sure_flag: false,
      checkemail_flag: false,
//      data
      login_username: '',
      login_password: '',
      register_username: '',
      register_password: '',
      register_password_sure: '',
      register_email: '',
//      data_show
      user_name: '',
      user_email: '',
      log_img_text: '登TM的',
    }
  },
  mounted() {
    let that = this;
    that.user_name = sessionStorage.getItem("username");
    that.user_email = sessionStorage.getItem("email");
    if (that.user_name){
      that.logIn_flag = true;
    }else {
      that.logIn_flag = false;
    }
  },
  methods: {
    showLogIn () {
      let that = this;
      that.mine_flag = false;
      that.log_flag = true;
      that.log_form_flag = true;
      that.register_form_flag = false;
      that.log_img_text = '登TM的';
    },
    showLogUp () {
      let that = this;
      that.log_form_flag = false;
      that.register_form_flag = true;
      that.log_img_text = '注TM的';
    },
    cancel () {
      let that = this;
      that.mine_flag = true;
      that.log_flag = false;
    },
    //检查输入是否合法
    checkName () {
      let that = this;
      if (that.register_username == ''){
        that.checkname_flag = true;
      }else {
        that.checkname_flag = false;
      }
    },
    checkPassword () {
      let that = this;
      if (that.register_password.length < 6){
        that.checkpassword_flag = true;
      }else {
        that.checkpassword_flag = false;
      }
    },
    checkSurePassword () {
      let that = this;
      if (that.register_password != that.register_password_sure){
        that.checkpassword_sure_flag = true;
      }else {
        that.checkpassword_sure_flag = false;
      }
    },
    checkEmail () {
      let that = this;
      let re = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/;
      if (!re.test(that.register_email)){
        that.checkemail_flag = true;
      }else {
        that.checkemail_flag = false;
      }
    },
    //注册&登录&退出登录
    logUp () {
      let that = this;
      let data = {
        username: that.register_username,
        password: that.register_password,
        email: that.register_email
      };
      axios.post(AJAXURL + 'log_up',
        qs.stringify(data),
        {headers: {'Content-Type': 'application/x-www-form-urlencoded'}
      }).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {
          that.$toast.center('注册成功');
          that.login_username = that.register_username;
          that.login_password = that.register_password;
          that.log_form_flag = true;
          that.register_form_flag = false;
        } else {
          alert('注册失败,'+response.msg);
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
          sessionStorage.setItem("username", response.username);
          sessionStorage.setItem("userid", response.userid);
          sessionStorage.setItem("email", response.email);
          that.user_name = response.username;
          that.user_email = response.email;
          that.$toast.center('登录成功');
          that.mine_flag = true;
          that.logIn_flag = true;
          that.log_flag = false;
        } else {
          alert(response.msg);
        }
      })
    },
    logOut () {
      let that = this;
      axios.get(AJAXURL + 'log_out',{}).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {
          that.$toast.center('登出');
          sessionStorage.removeItem('username');
          sessionStorage.removeItem('userid');
          sessionStorage.removeItem('email');
          that.user_name = '';
          that.user_email = '';
          that.logIn_flag = false;
        } else {
          alert(response.msg);
        }
      })
    },
  }
}
</script>

<style scoped>
  .mine { width: 100%; margin-bottom: 200px; }

  .mine-header { width: 100%; height: 220px;}

  .header-default { line-height: 220px; font-family: PingFangSC-Regular; font-size: 40px;  color: #FFF; background: #2c3e50;  letter-spacing: 0;  text-align: center; }

  .header-userinfo { width: 100%; height: 220px; padding-top: 20px; margin-left: 32px; background: #FFF; }

  .header-name { font-size:64px;  font-weight:bold;  color:#000; }

  .header-email {font-size:56px;  color:#000; }



  /*登录*/
  .log-img { width: 100%; height: 300px; line-height: 300px; font-size: 80px; text-align: center; background: #f0f7ff; border-bottom: 1px solid #666666; }

  .log-form { margin: 20px 32px; }

  .log-form-item { width: 606px;  height: 88px; margin: 40px auto; border: 1px solid #4779c6; border-radius: 15px;}

  .register-form-item { width: 606px;  height: 88px; margin: 40px auto; border: 1px solid #4779c6; border-radius: 15px;}

  .register-form-item p { margin: 20px 0 0 410px; font-size: 22px;  color: red;}

  .log-form-item input, .register-form-item input { width: 500px; height: 60px; margin: 10px 0 0 50px; border: none; font-family: PingFangSC-Regular;  font-size: 32px;  color: #999999;  letter-spacing: 0; }

  .log-btn, .cancel-btn, .register-btn, .logout-btn { width: 606px; height: 88px; line-height: 88px; margin: 10px auto; text-align: center;  border-radius: 15px; font-family: PingFangSC-Regular;  font-size: 32px;  letter-spacing: 0; }

  .log-btn { color: #FFF; background: #2db7f5; }

  .cancel-btn { color: #FFF; background: #ff4a21; }

  .register-btn { color: #2b85e4; border: 1px solid #2b85e4; }

  .logout-btn { color: #ed4014; border: 1px solid #ed4014; }

</style>
