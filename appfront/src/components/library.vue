<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input_add" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template slot-scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template slot-scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="100">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
    </el-row>
    <el-row>

    </el-row>
  </div>
</template>

<script>/* eslint-disable */
  import axios from 'axios'
  import { AJAXURL } from '../define.js'
import ElRow from "element-ui/packages/row/src/row";
export default {
  components: {ElRow},
  name: 'library',
  data () {
    return {
      input_add: '',
      bookList: []
    }
  },
  mounted: function () {
    this.showAllBooks()
  },
  methods: {
    showAllBooks: function () {
      let that = this;
      axios.post(AJAXURL + 'show_books',{}).then(function (res) {
        let response = res.data;
        if (response.error_num == 0){
          that.bookList = response.list
        }else {
          that.$message.error('查找失败')
          console.log(response['msg'])
        }
      })
    },
    addBook: function () {
      let that = this;
      if (that.input_add != ''){
         axios.get(AJAXURL + 'add_book?book_name=' + that.input_add).then(function (res) {
           let response = res.data;
           if (response.error_num == 0){
             that.$message.success('新增书籍成功');
             that.showAllBooks();
           }else {
             that.$message.error('新增书籍失败，请重试')
             console.log(response['msg'])
           }
         })
      }
    },
    handleClick: function (row) {
      let that = this;
      let id = row.pk;
       axios.get(AJAXURL + 'delete_book?id=' + id).then(function (res) {
           let response = res.data;
           if (response.error_num == 0){
             that.$message.success('删除书籍成功');
             that.showAllBooks();
           }else {
             that.$message.error('删除书籍失败，请重试')
             console.log(response['msg'])
           }
         })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
