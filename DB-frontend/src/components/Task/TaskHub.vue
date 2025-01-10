<template>
  <div style="margin-top: -50px;">
    <loading v-if="loading"/>
    <v-container v-else>
      <v-container>
        <v-card outlined class="pa-2 top">
          <div class="filters">
            <v-row class="align-center my-0 py-0">
              <v-col cols="auto" class="my-0 py-0">
                <span><strong>排序</strong>:</span>
              </v-col>
              <v-col class="my-0 py-0">
                <span @click="setFilter('sort_by', 0)"
                  :class="{ active: filters.sort_by === 0 }">综合</span>
                <!-- <span @click="setFilter('sort_by', 1)"
                  :class="{ active: filters.sort_by === 1 }"></span> -->
                <span @click="setFilter('sort_by', 4)"
                  :class="{ active: filters.sort_by === 4 }">悬赏金额</span>
                <span @click="setFilter('sort_by', 2)"
                  :class="{ active: filters.sort_by === 2 }">最近创建</span>
                <!-- <span @click="setFilter('sort_by', 3)"
                  :class="{ active: filters.sort_by === 3 }">最近回答</span> -->
              </v-col>
            </v-row>
            <v-row class="align-center my-0 py-0">
              <v-col cols="auto" class="my-0 py-0 mr-0 pr-0">
                <span><strong>标签筛选</strong>:</span>
              </v-col>
              <v-col class="my-0 py-0 ml-0 pl-0">
                <v-chip-group multiple column active-class="active-tag" class="my-0 py-0">
                  <v-chip v-for="(tag, index) in availableTags" :key="index"
                    :color="getTagColor(tag)"
                    class="my-1 py-0"
                    outlined @click="toggleTag(tag)">
                    {{ tag }}
                  </v-chip>
                </v-chip-group>
              </v-col>
            </v-row>
          </div>
          <!-- 底部的搜索栏 -->
          <v-divider></v-divider>
          <v-row class="mt-0">
            <v-col>
              <v-text-field v-model="filters.key_word" label="请输入搜索内容" placeholder="" filled
                append-icon="mdi-magnify" hide-details :loading="silentLoading"></v-text-field>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
      <v-container>
        <v-row no-gutters>
          <v-card class="card" v-for="(item, index) in cards" :key="index" @click="tryOpenItem(item)" :disabled="silentLoading">
            <div class="ma-0 pa-0">
              <div style="display: flex; align-items: center;">
                <h3 style="margin: 0; padding: 0;">{{ item.title }}</h3>
                <v-icon v-if="item.commission > 0" color="#F8CC00" style="margin-left: 8px;">mdi-bitcoin</v-icon>
                <span v-if="item.commission > 0" style="font-size: 13px; color: #666666; margin-left: 0.2%;">
                  {{ item.commission }} 菜币
                </span>
              </div>
              <span class="ml-2">{{ filterString(item.tiny_content) }}</span>
              <v-chip-group column class="ma-0 pa-0">
                <v-chip
                  v-for="(tag, idx) in item.tags"
                  :key="idx"
                  :color="getTagColor(tag)"
                  outlined
                  class="ma-1 py-0"
                >
                  {{ tag }}
                </v-chip>
              </v-chip-group>
            </div>
            <div class="pa-0 ma-0">
              <span style="font-size: 14px;">发布于: {{ format(item.created_at, 'yyyy-MM-dd HH:mm:ss') }}</span>
              <v-avatar size="20" class="mr-2">
                <img :src="item.created_by.avatar" alt="avatar">
              </v-avatar>
              <a :href="`/center/${item.created_by.user_id}`" @click.stop style="font-size: 16px;" target="blank">{{ item.created_by.username }}</a>
            </div>
            <div class="action-buttons" v-if="$store.state._role_ === 'Administrator'">
              <v-btn color="red" icon @click.stop="tryDelete(item)">
                <v-icon style="font-size: 32px;">mdi-delete</v-icon>
              </v-btn>
            </div>
          </v-card>
        </v-row>
      </v-container>
      <v-pagination
        v-if="totalPages >= 1"
        v-model="currentPage"
        :length="totalPages"
        @input="getTasks"
      />
    </v-container>
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="headline">确认删除</v-card-title>
        <v-card-text>你确定要删除这个任务吗？此操作无法撤销。</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="deleteDialog = false">取消</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import loading from "../Loading.vue";
import { format } from "date-fns";
export default {
  name: 'ShareHub',
  components: {
    loading,
    format,
  },
  data() {
    return {
      silentLoading: false,
      totalPages: 0,
      currentPage: 1,
      deleteDialog: false,
      loading: true,
      filters: {
        sort_by: 0,
        pay: 0,
        key_word: '',
        tags: [],
      },
      availableTags: [],
      filtersChanged: false, // 用来标记 filters 是否有变化
      curItem: null,
      cards: [],
    };
  },
  watch: {
    filters: {
      deep: true, // 深度监听对象
      handler() {
        this.filtersChanged = true;
      },
    },
  },
  methods: {
    format,
    onCardMouseLeave() {
      if (this.filtersChanged) {
        // 如果 filters 有变化，就重新获取数据
        this.currentPage = 1;
        this.getTasks();
        this.filtersChanged = false; // 重置变化标记
      }
    },
    setFilter(type, value) {
      this.filters[type] = value;
    },
    getTasks() {
      this.silentLoading = true;
      const p = {
        key_word: this.filters.key_word,
        tags: this.filters.tags,
        sort_by: this.filters.sort_by,
        pay: this.filters.pay,
        page: this.currentPage,
      }
      this.$store.dispatch("getTasks", p)
        .then((res) => {
          this.totalPages = res.total_page;
          this.cards = res.posts;
          this.loading = false;
          this.silentLoading = false;
        })
        .catch((error) => { this.$store.commit("setAlert", { type: "error", message: error, }); })
    },
    getTagColor(tag) {
      return this.filters.tags.includes(tag) ? 'blue accent-2' : 'brown';
    },
    toggleTag(tag) {
      const index = this.filters.tags.indexOf(tag);
      if (index === -1) {
        // 如果标签未被选中，则添加到 filters.tags
        this.filters.tags.push(tag);
      } else {
        // 如果标签已被选中，则移除
        this.filters.tags.splice(index, 1);
      }
    },
    tryOpenItem(item) {
      this.curItem = item;
      window.open(`/tasks/${item.mission_id}`, '_blank');
    },
    tryDelete(item) {
      this.curItem = item;
      this.deleteDialog = true;
    },
    filterString(inputText) {
      // 使用正则表达式替换掉所有的*和#符号
      return inputText.replace(/[\*\#]/g, '');
    },
    confirmDelete() {
      this.$store.dispatch("deleteTask", this.curItem.mission_id)
        .then(() => {
          this.$store.commit("setAlert", { type: "success", message: "删除成功", });
          this.cards = this.cards.filter((card) => card.mission_id !== this.curItem.mission_id);
        })
        .catch((error) => {
          this.$store.commit("setAlert", { type: "error", message: error, });
        });
    },
  },
  mounted() {
    this.loading = true;
    this.$store.commit("setAppTitle", "共享资源站");
    this.$store.dispatch("getTags", {key_word: null})
      .then((tags) => {
        this.availableTags = tags.tags;
      })
      .catch((error) => {
        this.$store.commit("setAlert", {
          type: "error",
          message: error,
        });
      });
    this.getTasks();
    this.interval = setInterval(this.onCardMouseLeave, 500);
  },
  beforeDestroy() {
    // 在组件销毁前清除定时器
    clearInterval(this.interval);
  },
};
</script>

<style scoped>
.top {
  border-width: 3px !important;
  /* 只改变边框粗细 */
  border-style: solid;
  border-radius: 5px;
  /* 可选，增加圆角效果 */
}

span {
  cursor: pointer;
  margin-right: 20px;
  color: gray;
}

.active {
  color: orange;
}

.filters {
  padding: 10px;
  /* 内边距 */
  display: inline-block;
  /* 确保 span 是块元素，并且 padding 生效 */
}

.tag {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 10px;
  margin: 0 5px;
  width: max-content;
  height: 20px;
  font-size: 12px;
  font-family: 'AlibabaPuHuiTi-3-55-Regular', sans-serif;
  color: #3d3d3d;
  background: #12a528;
  border-radius: 10px;
}

.picture {
  padding-left: 1%;
  padding-top: 0.3%;
  padding-bottom: 0.1%;
}


.card-container {
  position: relative;
  display: flex;
  align-items: center;
}

.card-content {
  transition: transform 0.3s ease;
  width: 100%;
}


.action-buttons {
  position: absolute;
  bottom: 30px;
  right: 14px;
  display: flex;
  align-items: center;
  opacity: 0;
  z-index: 1111; /* 确保按钮位于其他元素之上 */
  transition: opacity 0.2s ease-in-out;
}

.action-buttons:hover {
  opacity: 1;
}

.row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.card {
  position: relative;
  flex: 0 0 48%;
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}


.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.tag {
  padding: 3px 8px;
  border-radius: 3px;
  color: #fff;
  font-size: 12px;
}

.highlight {
  background-color: red;
}

.info {
  background-color: blue;
}

.normal {
  background-color: green;
}

.details {
  font-size: 12px;
  color: #999;
}

.card-middle {
  margin: 10px 0;
  font-size: 14px;
  color: #666;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  color: orange;
}
</style>