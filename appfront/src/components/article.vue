<template>
  <div class="home">
    <el-container>
      <el-main style="border-right: 1px solid #999">
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
                    <el-button type="primary" icon="el-icon-caret-top" circle></el-button>
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
            <div class="commentBox">
              <div class="commentAdd">
                <el-row class="add_continer">
                  <el-input class="article_body_input" v-model="input_comment" placeholder="写评论" style="width: 90%"></el-input>
                  <el-button type="primary" @click="addArticle_comment(item.pk)" style="float:right; margin: 2px;">评论</el-button>
                </el-row>
              </div>
              <div class="commentBody">
                <el-button type="primary" @click="showArticle_comment(item.pk)" style="margin: 2px;">评论</el-button>
                  <div class="comment_text" v-for="value in comment_list">
                      <div class="comment_user">{{ value.fields.comment_username }}</div>
                      <div class="comment_time">{{ value.fields.add_time }}</div>
                      <div class="comment_body">{{ value.fields.comment_body}}</div>
                  </div>
              </div>
            </div>
          </div>
        </el-row>
      </el-main>
      <el-aside width="300px" style="padding-left: 10px">
        <el-row class="add_continer">
          <p>写文章:</p>
          <el-input class="article_title_input" type="textarea" :rows="1" v-model="input_title" placeholder="文章标题"></el-input>
          <el-input class="article_body_input" type="textarea" :rows="4" v-model="input_body" placeholder="文章主体"></el-input>
          <el-button type="primary" @click="addArticle()" style="float:left; margin: 2px;">发布</el-button>
        </el-row>
      </el-aside>
    </el-container>
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
  name: 'article_add',
  data () {
    return {
      input_title: '',
      input_body: '',
      input_comment: '',
      article_list: [],
      comment_list: []
    }
  },
  mounted: function () {
    this.showAllArticals()
  },
  methods: {
    showAllArticals: function () {
      let that = this;
      axios.get(AJAXURL + 'show_articles').then(function (res) {
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
    addArticle: function () {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      if (that.input_title != ''){
         axios.get(AJAXURL + 'add_article',{
           params: {
             article_title: that.input_title,
             article_body: that.input_body,
             article_user: article_user
           }
         }).then(function (res) {
           let response = res.data;
           if (response.error_num == 0){
             that.$message.success('发布成功');
             that.showAllArticals();
             that.input_title = '';
             that.input_body = '';
           }else {
             that.$message.error('发布失败，请重试')
             console.log(response['msg'])
           }
         })
      }
    },
    deleteArticle: function (id) {
      let that = this;
      axios.get(AJAXURL + 'delete_article?id=' + id).then(function (res) {
          let response = res.data;
          if (response.error_num == 0) {
            that.$message.success('删除成功');
            that.showAllArticals();
          } else {
            that.$message.error('删除失败，请重试')
            console.log(response['msg'])
          }
        })
      },
    addArticle_comment(article_id) {
      let that = this;
      let username = sessionStorage.getItem("username");
      let data = {};
      if (username){
        data = {
          article_id: article_id,
          comment_body: that.input_comment,
          comment_username: sessionStorage.getItem("username")
        };
      }else {
        data = {
          article_id: article_id,
          comment_body: that.input_comment
        }
      }
      axios.post(AJAXURL + 'add_comment',
        qs.stringify(data),
        {
          headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).then(function (res) {
        let response = res.data;
        if (response.error_num == 0) {

        } else {
          that.$message.error('评论失败,' + response.msg);
          console.log(response['msg'])
        }
      })
    },
    showArticle_comment(article_id){
      let that = this;
      axios.get(AJAXURL + 'show_comment?article_id=' + article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          _.forEach(response.list, function (item) {
            item.fields.add_time = item.fields.add_time.slice(0,10);
          })
          that.comment_list = response.list;
        }else {
          that.$message.error('查找失败')
          console.log(response['msg'])
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
  .commentBox {
    border-top: 1px solid #777;
  }
  .comment_text {
    border: 1px solid #888;
  }
  .comment_user {
    width: 50%;
    float: left;
    display: inline-block;
    border-bottom: 1px solid #00ffff;
  }
  .comment_time {
    width: 50%;
    float: right;
    display: inline-block;
    border-bottom: 1px solid #00ffff;
  }
  .comment_body {

  }
</style>
