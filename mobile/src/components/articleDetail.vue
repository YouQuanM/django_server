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
      <div class="article-comment" @click="comment()">评论</div>
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
      article_id : '',
      article_title: '',
      article_body: '',
      article_praise: '',
      article_time: '',
      isUser: false,
      comment_list: []
    }
  },
  mounted: function () {
    this.articleLoad();
  },
  methods: {
    articleLoad(){
      let that = this;
      that.showArticleComment(that.$route.query.id);
      that.article_id = that.$route.query.id;
    },
    showArticleComment (article_id){
      let that = this;
      //获取文章
      axios.get(AJAXURL + 'show_articles?article_id=' + article_id).then(function (res) {
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
      axios.get(AJAXURL + 'show_comment?article_id=' + article_id).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          _.forEach(response.list, function (item) {
            item.fields.add_time = item.fields.add_time.slice(0,10);
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
            that.showAllArticals();
          } else {
            that.$toast.center('删除失败，请重试')
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
          that.showArticle_comment(article_id)
        } else {
          that.$toast.center('评论失败,' + response.msg);
          console.log(response['msg'])
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
    comment() {
      alert("维护中,别乱动");
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

</style>
