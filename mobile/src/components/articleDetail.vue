<template>
  <div class="article-detail">
    <div class="article-title">
      {{ article_title }}
    </div>
    <div class="article-body">
      <div class="article-content">
        {{ article_body }}
      </div>
      <div class="article-time">
        {{ article_time }}
      </div>
    </div>
    <div class="article-comment-body">
      <div class="comment-title">
        评论
      </div>
      <div class="comment-list">
        <div class="comment-item" v-for="item in comment_list">
          <div class="comment-user">
            {{ item.fields.comment_username }}:
          </div>
          <div class="comment-time">
            {{ item.fields.add_time }}
          </div>
          <div class="comment-content">
            {{ item.fields.comment_body }}
          </div>
        </div>
      </div>
    </div>
    <div class="article-footer">
      <div class="article-praise" v-if="!isUser" @click="articlePraise()">点赞 {{ article_praise }}</div>
      <div class="article-delete" v-if="isUser" @click="deleteArticle()">删除</div>
      <div class="article-comment" @click="showAdd_comment()">评论</div>
    </div>
    <div class="article-comment-write" v-if="comment_flag">
      <div class="write-content">
        <div class="comment-write-name">{{ comment_userName }}</div>
        <div class="comment-write-body">
          <input type="text" v-model="input_comment" placeholder="吐槽吧">
        </div>
        <div class="comment-btn-group">
          <div class="comment-cancel-btn" @click="cancelComment">取消</div>
          <div class="comment-submit-btn" @click="addArticle_comment">确定</div>
        </div>
      </div>
      <div class="mask" @click="cancelComment"></div>

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'articleDetail',
  data () {
    return {
//      flag
      comment_flag: false,
//      data
      article_id : '',
      article_title: '',
      article_body: '',
      article_praise: '',
      article_time: '',
      isUser: false,
      comment_list: [],
      comment_userName: '匿名者',
      input_comment: ''
    }
  },
  mounted: function () {
    this.articleLoad();
  },
  methods: {
    articleLoad(){
      let that = this;
      that.article_id = that.$route.query.id;
      that.showArticleComment(that.$route.query.id);
    },
    showArticleComment (){
      let that = this;
      //获取文章
      axios.get(AJAXURL + 'show_articles?article_id=' + that.article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          let date = response.list[0].fields.add_time.slice(0,10);
          let time = response.list[0].fields.add_time.slice(11,16);
          that.article_time = date + " " + time;
          that.article_title = response.list[0].fields.article_title;
          that.article_body = response.list[0].fields.article_body;
          that.article_praise = response.list[0].fields.article_praise;
          if (response.list[0].fields.article_userid == sessionStorage.getItem("userid")){
            that.isUser = true;
          }else {
            that.isUser = false;
          }
        }else {
          that.$toast.center('查找失败');
          console.log(response['msg']);
        }
      });
      //获取评论
      axios.get(AJAXURL + 'show_comment?article_id=' + that.article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          _.forEach(response.list, function (item) {
            item.fields.add_time = item.fields.add_time.slice(5,10) + ' ' + item.fields.add_time.slice(11,16);
          });
          that.comment_list = response.list;
          console.log(that.comment_list)
        }else {
          that.$toast.center('查找失败');
          console.log(response['msg'])
        }
      })
    },
    deleteArticle: function () {
      let that = this;
      axios.get(AJAXURL + 'delete_article?id=' + that.article_id).then(function (res) {
          let response = res.data;
          if (response.error_num == 0) {
            that.$toast.center('删除成功');
            that.$router.replace('/marticle');//跳转写文章页面
          } else {
            that.$toast.center('删除失败，请重试')
            console.log(response['msg'])
          }
        })
      },
    showAdd_comment (){
      let that = this;
      let username = sessionStorage.getItem("username");
      if (username){
        that.comment_userName = username;
      }
      that.comment_flag = true;
    },
    addArticle_comment() {
      let that = this;
      let username = sessionStorage.getItem("username");
      let data = {};
      if (username){
        data = {
          article_id: that.article_id,
          comment_body: that.input_comment,
          comment_username: sessionStorage.getItem("username")
        };
      }else {
        data = {
          article_id: that.article_id,
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
          that.articleLoad();
          that.comment_flag = false;
        } else {
          that.$toast.center('评论失败,' + response.msg);
          console.log(response['msg'])
          that.comment_flag = false;
        }
      })
    },
    articlePraise(){
      let that = this;
      axios.get(AJAXURL + 'add_praise?article_id=' + that.article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          that.showArticleComment(that.article_id);
        }else {
          that.$toast.center('点赞失败');
          console.log(response['msg'])
        }
      })
    },
    cancelComment(){
      let that = this;
      that.comment_flag = false;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .article-detail { width: 100%; }

  .article-title { padding: 30px 32px; border-bottom: 1px solid #666666; font-size: 36px; font-weight: bold; color: #464c5b; background: #FFF; }

  .article-content { margin: 30px 32px; line-height: 40px; font-size: 32px; color: #657180; background: #FFF;}

  .article-time { float: right;  margin: 0 32px 0 0; color: #9ea7b4; }

  .article-footer { position: fixed; bottom: 0; width: 100%; display: flex; flex-direction: row; }

  .article-praise, .article-delete, .article-comment{ width: 50%; }

  .article-praise { height: 100px; line-height: 100px; background: #2d8cf0; font-size: 40px; color: #FFF; text-align: center;}

  .article-delete { height: 100px; line-height: 100px; background: #ed4014; font-size: 40px; color: #FFF; text-align: center;}

  .article-comment { height: 100px; line-height: 100px; background: #19be6b; font-size: 40px; color: #FFF; text-align: center;}

  /*评论*/
  .article-comment-body { margin: 100px 32px; }

  .comment-item { border-bottom: 1px solid #9ea7b4; }

  .comment-title { padding: 30px 0; font-size: 36px; font-weight: bold; color: #464c5b; background: #FFF; }

  .comment-user { margin: 10px 0; font-size: 30px; font-weight: bold; color: #464c5b;}

  .comment-content { margin: 10px 0; font-size: 30px; color: #657180; }

  .comment-time { float: right; font-size: 26px;}

  /*写评论*/

  .article-comment-write { background: #FFF; height: 300px;}

  .article-comment-write .mask { width: 100%; height: 100%; position: fixed; top: 0; left: 0; background: rgba(102, 102, 102, 0.59); }

  .write-content { width: 100%; height: 200px; position: fixed; bottom: 100px; background: #FFF; z-index: 10; }

  .comment-write-name { padding: 30px 32px;  font-size: 36px;  font-weight: bold;  color: #464c5b;  background: #FFF;}

  .comment-write-body input { padding: 0 32px; width: 100%; height: 100px; margin: 0 auto; font-size: 28px;}

  .comment-btn-group { display: flex; flex-direction: row; height: 100px; width: 100%; }

  .comment-cancel-btn, .comment-submit-btn { width: 50%; height: 100px; line-height: 100px; text-align: center; font-size: 40px; color: #FFF;}

  .comment-cancel-btn { background: #999999; }

  .comment-submit-btn { background: #19be6b; }
</style>
