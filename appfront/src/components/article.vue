<template>
  <div class="home">
    <el-container>
      <el-main style="border-right: 1px solid #999">
        <el-row>
          <div class="article_continer" :key="item.pk" v-for="item in article_list">
            <el-card :body-style="{ padding: '0px' }" shadow="hover">
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
            <el-button type="primary" @click="showArticle_comment(item.pk)" style="margin: 2px;">评论</el-button>
            <el-button type="primary" @click="showCommentFlag = ''" style="margin: 2px;" v-if="showCommentFlag == item.pk">收起</el-button>
            <div class="commentBox" v-if="showCommentFlag == item.pk">
              <div class="commentAdd">
                <el-row class="add_continer">
                  <el-input class="article_body_input" v-model="input_comment" placeholder="写评论" style="width: 90%"></el-input>
                  <el-button type="primary" @click="addArticle_comment(item.pk)" style="float:right; margin: 2px;">评论</el-button>
                </el-row>
              </div>
              <div class="commentBody">
                <div class="comment_text" :key="value.pk" v-for="value in comment_list">
                  <div class="comment_user">{{ value.fields.comment_username }}</div>
                  <div class="comment_time">{{ value.fields.add_time }}</div>
                  <div class="comment_body">{{ value.fields.comment_body}}</div>
                </div>
              </div>
            </div>
            </el-card>
          </div>
        </el-row>
      </el-main>
      <el-aside width="300px" style="padding-left: 10px">
        <el-row class="add_continer">
          <p>写文章:</p>
          <!--<div>            &lt;!&ndash; 组件有两个属性 value 传入内容双向绑定 setting传入配置信息 &ndash;&gt;-->
            <!--<editor class="editor" :value="content"  :setting="editorSetting" @input="(content)=> content = content"></editor>-->
          <!--</div>-->
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
  import qs from 'qs';
//  import editor from '@/modules/editor'

export default {
  components: {
    ElRow,
//    'editor':editor
  },
  name: 'article_add',
  data () {
    return {
      input_title: '',
      input_body: '',
      input_comment: '',
      article_list: [],
      comment_list: [],
      showCommentFlag: ''
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
            let date = item.fields.add_time.slice(0,10);
            let time = item.fields.add_time.slice(11,19);
            item.fields.add_time = date + " " + time;
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
      let article_userid = sessionStorage.getItem("userid");
      if (!article_userid){
        that.$message.error('请先登录')
      }else {
        if (that.input_title != ''){
         axios.get(AJAXURL + 'add_article',{
           params: {
             article_title: that.input_title,
             article_body: that.input_body,
             article_user: article_user,
             article_userid: article_userid
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
          });
          that.comment_list = response.list;
          that.input_comment = '';
          that.showCommentFlag = article_id;
        }else {
          that.$message.error('查找失败');
          console.log(response['msg'])
        }
      })
    },
    articlePraise(article_id){
      let that = this;
      axios.get(AJAXURL + 'add_praise?article_id=' + article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          that.showAllArticals();
        }else {
          that.$message.error('点赞失败');
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
    margin: 15px auto;
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
    padding: 15px;
    border-top: 1px solid rgba(119, 119, 119, 0.35);
    border-bottom: 1px solid rgba(119, 119, 119, 0.35);
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
