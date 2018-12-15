<template>
  <div class="marticle">
    <div class="marticle-group">
      <div class="marticle-items" :key="item.pk" v-for="item in article_list" @click="toDetail(item.pk)">
        <div class="marticle-title">{{ item.fields.article_title }}</div>
        <div class="marticle-body">{{ item.fields.article_body }}</div>
        <div class="marticle-info">
          <div class="marticle-praise">{{ item.fields.article_praise }}赞同</div>
          <div class="marticle-user">作者:{{ item.fields.article_user }}</div>
          <div class="marticle-time">{{ item.fields.add_time }}</div>
        </div>
      </div>
    </div>
    <div class="write-btn" @click="toWriteArticle()">
      写文章
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'marticle',
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
            let time = item.fields.add_time.slice(11,16);
            item.fields.add_time = date + " " + time;
          });
          that.article_list = response.list
        }else {
          that.$toast.center('查找失败')
          console.log(response['msg'])
        }
      })
    },
    addArticle: function () {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      let article_userid = sessionStorage.getItem("userid");
      if (!article_userid){
        that.$toast.center('请先登录')
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
             that.$toast.center('发布失败，请重试')
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
          that.$toast.center('查找失败');
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
          that.$toast.center('点赞失败');
          console.log(response['msg'])
        }
      })
    },
    toWriteArticle() {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      if (article_user){
        that.$router.replace({ path: '/writeArticle'});//跳转写文章页面
      }else {
        that.$toast.center('请先登录')
      }
    },
    toDetail(id) {
      let that = this;
      that.$router.push({ path: '/articleDetail', query:{ id: id }});//跳转写文章页面
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .marticle { width: 100%; background: #f8f8f9; }

  .marticle-group { margin: 10px 0; }

  .marticle-items { margin: 10px 0; padding: 0 32px; background: #FFF; }

  .marticle-title { margin: 10px 0; padding: 10px 0 0 0; font-size: 36px;  font-weight: bold;  color: #464c5b; }

  .marticle-body { font-size: 26px; color: #657180; }

  .marticle-info { display: flex; flex-direction: row; width: 100%; margin: 10px 0; }

  .marticle-praise, .marticle-user, .marticle-time { font-size: 26px; color: #9ea7b4;}

  .marticle-praise { width: 30%; }

  .marticle-user { width: 30%; }

  .marticle-time { width: 40%; }

  .write-btn { width: 100px; height: 100px; line-height: 100px; position: fixed; bottom: 200px; right: 32px; border-radius: 50px; font-size: 33px; font-weight: bold; background: #5cadff; }

</style>
