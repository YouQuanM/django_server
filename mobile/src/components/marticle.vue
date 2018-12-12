<template>
  <div class="article_continer" style="padding-bottom: 50px">
    <div class="article" :key="item.pk" v-for="item in article_list">
      <card>
        <h3 class="card-padding" slot="header" style="width:100%;display:block;">{{ item.fields.article_title }}</h3>
        <div slot="content" class="card-padding">
          {{ item.fields.article_body }}
        </div>
        <div slot="content" class="card-demo-flex card-demo-content01">
          <div class="vux-1px-r">
            <x-button mini @click.native="articlePraise(item.pk)">
              <x-icon type="ios-arrow-up" size="30"></x-icon>
              {{ item.fields.article_praise }}
            </x-button>
            <br/>
          </div>
          <div class="vux-1px-r">
            <x-button mini @click.native="showArticle_comment(item.pk)">
              评论
            </x-button>
            <br/>
          </div>
          <div class="vux-1px-r">
            {{ item.fields.article_user }}
            <br/>
          </div>
          <div>
            {{ item.fields.add_time }}
            <br/>
          </div>
        </div>
        <div class="comment" slot="content" v-if="showCommentFlag == item.pk">
          <x-button @click.native="showCommentFlag = ''" style="margin: 2px;" v-if="showCommentFlag == item.pk">收起</x-button>
          <br/>
          <div class="commentBody">
            <div class="comment_text" :key="value.pk" v-for="value in comment_list">
              <div class="comment_user">{{ value.fields.comment_username }}</div>
              <div class="comment_time">{{ value.fields.add_time }}</div>
              <div class="comment_body">{{ value.fields.comment_body}}</div>
            </div>
          </div>
          <x-input class="article_body_input" v-model="input_comment" placeholder="写评论" style="width: 90%"></x-input>
          <x-button type="primary" @click.native="addArticle_comment(item.pk)">评论</x-button>
        </div>
      </card>
    </div>
    <div class="toWriteArticel">
      <div class="writeButton" @click="toWriteArticle()">写文章</div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
  let _ = require('lodash');
  import qs from 'qs';
  import { Card,XButton,XInput } from 'vux';
export default {
  components: {
    Card,XButton,XInput
  },
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
          that.showArticle_comment(article_id)
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
    },
    toWriteArticle() {
      let that = this;
      let article_user = sessionStorage.getItem("username");
      if (article_user){
        that.$router.push({ path: '/writeArticle'});//跳转写文章页面
      }else {
        alert('请先登录')
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .article_continer {
    margin: 15px auto;
  }
  .card-demo-flex {
  display: flex;
}
.card-demo-content01 {
  padding: 10px 0;
}
.card-padding {
  padding: 15px;
}
.card-demo-flex > div {
  flex: 1;
  text-align: center;
  font-size: 12px;
}
.card-demo-flex span {
  color: #f74c31;
}
  .commentBody {
    background: #ccc;
  }
  .comment_text {
    border-bottom: 1px solid #f0f7ff;
  }
  .comment_user,.comment_time,.comment_body {
    margin-left: 10px;
  }
  .comment_time {
    float: right;
  }
  .toWriteArticel {
    width: 50px;
    height: 50px;
    position: fixed;
    bottom: 100px;
    right: 10px;
  }
  .writeButton {
    width: 40px;
    height: 30px;
    padding-top: 10px;
    background: #8cf3ff;
    border-radius: 20px;
    font-size: 13px;
  }
</style>
