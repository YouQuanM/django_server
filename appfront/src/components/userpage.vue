<template>
  <div class="userpage">
    <el-row :gutter="20">
      <el-col :span="16" style="border-right: 1px solid #777">
        <div class="grid-content bg-purple">
          <div class="user_articles">
          <el-row>
            <div class="article_continer" :key="item.pk" v-for="item in article_list">
              <el-row>
                <el-col :span="12">
                  <div class="article_title">
                    <h3 class="title_text">title:</h3>
                    <div style="display: inline">{{ item.fields.article_title }}</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="article_user">
                    <h3 class="user_text">user:</h3>
                    <div style="display: inline">{{ item.fields.article_user }}</div>
                  </div>
                </el-col>
              </el-row>
              <div class="article_body">
                {{ item.fields.article_body }}
              </div>
              <div class="article_operate">
                <el-row>
                  <el-col :span="6">
                    <el-button type="primary" icon="el-icon-caret-top" circle @click="articlePraise(item.pk)"></el-button>
                    {{ item.fields.article_praise }}
                  </el-col>
                  <el-col :span="6">
                    <el-button type="primary" icon="el-icon-edit" circle></el-button>
                  </el-col>
                  <el-col :span="6">
                    <el-button type="danger" icon="el-icon-delete" @click="deleteArticle(item.pk)" circle></el-button>
                  </el-col>
                  <el-col :span="6">
                    <div class="grid-content bg-purple">
                      {{ item.fields.add_time }}
                    </div>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-row>
        </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="user_center">
          <div class="username">用户名：{{ username }}</div>
          <div class="changepassword">
            <div class="password_input">
              <el-input placeholder="请输入原密码" v-model="old_password" style="width: 250px">
                <template slot="prepend">原密码:</template>
              </el-input>
            </div>
            <div class="password_input">
              <el-input placeholder="请输入新密码" v-model="new_password" style="width: 250px">
                <template slot="prepend">新密码:</template>
              </el-input>
            </div>
            <el-button type="primary" plain @click="changePassword">修改密码</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>/* eslint-disable */
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  import ElRow from "element-ui/packages/row/src/row";
  let _ = require('lodash');
  import qs from 'qs'
export default {
  components: {ElRow},
  name: 'userpage',
  data () {
    return {
      username: '',
      article_list: [],
      old_password: '',
      new_password: ''
    }
  },
  mounted: function () {
    this.showAllArticals();
    this.getuserinfo()
  },
  methods: {
    showAllArticals () {
      let that = this,user = sessionStorage.getItem("username");
      axios.get(AJAXURL + 'show_articles?username=' + user).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          _.forEach(response.list,function (item) {
            item.fields.add_time = item.fields.add_time.slice(0,10)
          });
          that.article_list = response.list
        }else {
          that.$message.error('查找失败')
          console.log(response['msg'])
        }
      })
    },
    getuserinfo () {
      let that = this,article_user = sessionStorage.getItem("username");
      that.username = article_user;
    },
    changePassword () {
      let that = this;
      let userId = sessionStorage.getItem("userid");
      let data = {
        userid: userId,
        old_password: that.old_password,
        new_password: that.new_password
      };
      axios.post(AJAXURL + 'change_password', qs.stringify(data), {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          that.$message.success('修改成功');
          that.old_password = '';
          that.new_password = '';
        }else {
          that.$message.error(response.msg)
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .article_continer {
    border: 1px solid #666;
    margin: 10px auto;
  }
  .article_title {
    font-size: 20px;
  }
  .add_continer {
    margin-top: 20px;
  }
  .title_text,.user_text {
    display: inline;
  }
  .article_body {
    border-top: 1px solid #777;
    border-bottom: 1px solid #777;
  }
  .password_input {
    margin: 10px auto;
  }
</style>
