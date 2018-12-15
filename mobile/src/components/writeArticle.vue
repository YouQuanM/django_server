<template>
  <div class="write-article">
    <div class="write-article-header">
      <div class="header-title">
        {{ user_name }}说：
      </div>
    </div>
    <div class="write-article-content">
      <div class="content-title">
        <input type="text" v-model="article_title" placeholder="请输入标题">
      </div>
      <div class="content-body">
        <textarea v-model="article_body" placeholder="请输入内容"></textarea>
      </div>
    </div>
    <div class="write-article-btn">
      <div class="submit-btn" @click="addArticle()">确认</div>
      <div class="cancel-btn" @click="cancel()">取消</div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
export default {
  name: 'writeArticle',
  data () {
    return {
      user_name: '',
      article_title: '',
      article_body: ''
    }
  },
  created() {
    let that = this;
    that.user_name = sessionStorage.getItem("username");
  },
  methods: {
    addArticle () {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      let article_userid = sessionStorage.getItem("userid");
      if (that.article_title != ''){
       axios.get(AJAXURL + 'add_article',{
         params: {
           article_title: that.article_title,
           article_body: that.article_body,
           article_user: article_user,
           article_userid: article_userid
         }
       }).then(function (res) {
         let response = res.data;
         if (response.error_num == 0){
           that.$router.go(-1);//跳转写文章页面
           that.input_title = '';
           that.input_body = '';
         }else {
           that.$toast.center('发布失败，请重试')
           console.log(response['msg'])
         }
       })
    }else {
        that.$toast.center('标题不能为空')
      }
    },
    cancel() {
      let that = this;
      that.$router.replace('/marticle');
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .write-article { width: 100%; }

  .write-article-header { width: 100%; height: 100px; border-bottom: 1px solid #666666; }

  .header-title { height: 100px; line-height: 100px; margin-left: 30px; font-family: PingFangSC-Regular;  font-size: 56px;  color: #333333;  letter-spacing: 0.8px; }

  .write-article-content { padding: 40px 32px; }

  .content-title input, .content-body textarea { width: 100%; font-family: PingFangSC-Regular;  font-size: 32px;  color: #999999;  letter-spacing: 0; }

  .content-title { border-bottom: 1px solid #666666 }

  .content-title input { width: 666px; height: 100px; padding-left: 20px; line-height: 100px; background: #F7F8F9; border: none; }

  .content-body textarea { width: 646px; height: 530px; padding: 20px; background: #F7F8F9; border: none;}

  .submit-btn, .cancel-btn { width: 606px; height: 88px; line-height: 88px; margin: 10px auto; text-align: center;  border-radius: 15px; font-family: PingFangSC-Regular;  font-size: 32px;  color: #FFFFFF;  letter-spacing: 0; }

  .submit-btn { background: #19be6b; }

  .cancel-btn { color: #515a6e; background: #f8f8f9; border: 1px solid #dcdee2; }
</style>
