<template>
  <div id="app">
    <el-container>
      <el-header style="border-bottom: 1px solid #999">
        <div>
          <p style="display: inline">welcome</p>
          <h3 style="display: inline; margin: 0 500px">LIANGZHICOMPANY</h3>
          <!--登录按钮以及弹出框-->
          <el-popover
            placement="top"
            width="160"
            v-model="logInBox">
              <el-input v-model="login_username" placeholder="请输入用户名" :style="{display: logInFlag}"></el-input>
              <el-input v-model="login_password" placeholder="请输入密码" :style="{display: logInFlag}"></el-input>
              <el-button class="logInBoxBtn" type="primary" :style="{display: logSuccessFlag}">个人主页</el-button>
              <el-button class="logInBoxBtn" type="primary" :style="{display: logSuccessFlag}" @click="logOut">退出登录</el-button>
              <div style="text-align: right; margin: 0"  :style="{display: logInFlag}">
              <el-button size="mini" type="text" @click="dialogFormVisible = true">注册</el-button>
              <el-button type="primary" size="mini" @click="logIn">登录</el-button>
              </div>
              <el-button slot="reference">{{login_text}}</el-button>
          </el-popover>
        </div>
        <!--注册弹窗-->
        <el-dialog title="注册" :visible.sync="dialogFormVisible">
          <el-form :model="logup_from">
            <el-form-item label="用户名" :label-width="formLabelWidth">
              <el-input v-model="logup_from.username" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth">
              <el-input v-model="logup_from.password" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth">
              <el-input v-model="logup_from.email" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="logUp">确 定</el-button>
          </div>
        </el-dialog>
      </el-header>
      <el-container>
        <el-aside style="border-right: 1px solid #999" width="200px">
          <router-link to="/library">
            <el-button class="router_btn" type="primary">library</el-button>
          </router-link>
          <router-link to="/article">
            <el-button class="router_btn" type="primary">article</el-button>
          </router-link>
          <div>
            <img src="./assets/ququ.jpg" height="200" width="200"/>
          </div>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>/* eslint-disable */
import axios from 'axios'
import {AJAXURL} from './define.js'
import _ from 'lodash'
import ElRow from "element-ui/packages/row/src/row";
import qs from 'qs'
export default {
  components: {ElRow},
  name: 'App',
  data() {
    return {
      logInBox: false,
      login_username: '',
      login_password: '',
      login_text: '登录',
      dialogFormVisible: false,
      logup_from: {
        username: '',
        password: '',
        email: ''
      },
      formLabelWidth: '120px',
      logInFlag: 'block',
      logSuccessFlag: 'none'
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
          that.$message.success('欢迎');
          that.login_username = '';
          that.login_password = '';
          that.logInBox = false;
          that.login_text = response.userinfo;
          sessionStorage.setItem("username", response.userinfo);
          that.logInFlag = 'none';
          that.logSuccessFlag = 'block';
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
          that.login_text = '登录';
          that.logInFlag = 'block';
          that.logSuccessFlag = 'none';
        } else {
          that.$message.error(response.msg);
        }
      })
    }
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  .router_btn {
    margin: 10px;
  }
  .el-button+.el-button {
    margin-left: 0;
  }
  .logInBoxBtn {
    margin: 10px auto!important;
  }
</style>
