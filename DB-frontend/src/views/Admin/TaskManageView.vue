<template>
  <v-container class="spacing-playground pa-16" fluid>
    <div style="margin-top: -50px;">
      <template v-if="loading">
        <v-container fluid class="d-flex align-center justify-center">
          <v-row class="text-center">
            <v-col>
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            </v-col>
          </v-row>
        </v-container>
        <v-container fluid class="d-flex align-center justify-center">
          <v-row class="text-center">
            <v-col>
              <h3>
                潮平两岸阔，风正一帆悬。
              </h3>
              <h4>
                欢迎回到航U邦。
              </h4>
              <span>正在获取资源站。</span>
            </v-col>
          </v-row>
        </v-container>
      </template>
      <template v-else>
        <v-container>
          <v-card outlined class="pa-4 top"">
            <div class="filters">
              <v-row class="align-center">
                <v-col cols="auto">
                  <span><strong>排序</strong>:</span>
                </v-col>
                <v-col>
                  <span @click="setFilter('sort_by', 0)"
                    :class="{ active: filters.sort_by === 0 }">综合</span>
                  <!-- <span @click="setFilter('sort_by', 1)"
                    :class="{ active: filters.sort_by === 1 }"></span> -->
                  <span @click="setFilter('sort_by', 4)"
                    :class="{ active: filters.sort_by === 4 }">悬赏金额</span>
                  <span @click="setFilter('sort_by', 2)"
                    :class="{ active: filters.sort_by === 2 }">最近创建</span>
                  <span @click="setFilter('sort_by', 3)"
                    :class="{ active: filters.sort_by === 3 }">最近回答</span>
                </v-col>
              </v-row>
              <v-row class="align-center">
                <v-col cols="auto">
                  <span><strong>标签筛选</strong>:</span>
                </v-col>
                <v-col>
                  <v-chip-group v-model="filters.tags" multiple column active-class="active-tag">
                    <v-chip v-for="(tag, index) in availableTags" :key="index"
                      :color="getTagColor(tag)"
                      outlined @click="toggleTag(tag)">
                      {{ tag }}
                    </v-chip>
                  </v-chip-group>
                </v-col>
              </v-row>
            </div>
            <!-- 底部的搜索栏 -->
            <v-divider></v-divider>
            <v-row class="mt-4">
              <v-col>
                <v-text-field v-model="filters.search" label="请输入搜索内容" placeholder="" filled
                  append-icon="mdi-magnify" hide-details></v-text-field>
              </v-col>
            </v-row>
          </v-card>
        </v-container>
        <div class="container">
          <div class="row">
            <div class="card" v-for="(item, index) in cards" :key="index">
              <div class="card-body">
                <h3>{{ item.title }}</h3>
                <p>{{ item.tiny_content }}</p>
              </div>
              <div class="card-tags">
                <v-chip-group column>
                  <v-chip 
                    v-for="(tag, idx) in item.tags" 
                    :key="idx" 
                    :color="getTagColor(tag)" 
                    outlined
                  >
                    {{ tag }}
                  </v-chip>
                </v-chip-group>
              </div>
              <div class="card-middle">
                <span class="author">发布于: {{ item.created_at }}</span>
                <span class="author">发布者: {{ item.created_by.username }}</span>
                <v-icon v-if="item.commission > 0" color="#F8CC00">mdi-bitcoin</v-icon>
                <span v-if="item.commission > 0"
                  style="font-size: 13px; color: #666666; margin-left: 0.2%;">
                  {{ item.commission }} 菜币
                </span>
              </div>
              <!-- 操作按钮 -->
              <div class="action-buttons">
                <v-btn color="primary" class="me-2" icon @click.stop="openItem(item)">
                  <v-icon style="font-size: 32px;">mdi-open-in-new</v-icon>
                </v-btn>
                <v-btn color="red" icon @click.stop="deleteItem(item)">
                  <v-icon style="font-size: 32px;">mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'ShareHub',
  data() {
    return {
      loading: true,
      filters: {
        sort_by: 0,
        pay: 0,
        search: '',
        tags: [],
      },
      availableTags: [
        "计算机组成", "数据库", "面向对象", "测试", "考试题", "数据结构", "2023-2024", "2024-2025", "复习资料"
      ],
      filtersChanged: false, // 用来标记 filters 是否有变化
      curItem: null,
      cards: [
        {
          mission_id:0,
          title: "【任务发布】寻找全栈开发导师",
          tiny_content: "希望能找到一位有丰富全栈开发经验的导师，每周进行一次线上指导，帮助我解决学习中的问题并提供项目实践建议。感兴趣的请联系！",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["2024-2025", "复习资料"],
          commission: 12,
        },
        {
          mission_id:1,
          title: "【提问】如何优化后端接口性能？",
          tiny_content: "最近在开发一个电商项目，发现部分接口响应时间过长。主要使用的技术栈是Node.js + Express。请问有哪些优化建议，或者有没有类似的案例分享？",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 0,
        },
        {
          mission_id:2,
          title: "【求助】设计一个任务发布系统的数据库结构",
          tiny_content: "正在设计一个任务发布系统，涉及到用户、任务、评论等功能。希望能得到关于数据库表结构设计的具体建议，尤其是如何设计关联关系更合理。",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 1,
        },
        {
          mission_id:3,
          title: "【任务发布】前端设计优化需求",
          tiny_content: "需要一名熟悉Vue.js和UI/UX设计的开发者，帮助优化现有项目的用户界面，包括交互设计和性能提升。有兴趣的可以提交报价。",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 0,
        },
        {
          mission_id:3,
          title: "【提问】React和Vue如何选择？",
          tiny_content: "在开发一个中型项目时，团队对选择React还是Vue存在争议。请问这两者在性能、生态和学习成本上的主要差异是什么？希望大家能分享自己的经验。",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 10,
        },
        {
          mission_id:3,

          title: "【求助】后端服务高并发处理方案",
          tiny_content: "项目上线后访问量激增，后端服务器偶尔会崩溃。使用的技术栈是Java Spring Boot。请问有哪些可行的高并发处理方案？",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 20,
        },
        {
          mission_id:3,

          title: "【任务发布】短期项目外包——数据分析",
          tiny_content: "我们正在寻找一位熟悉Python和数据分析的开发者，负责处理并分析一组业务数据。项目周期为两周，具体细节可以私信商讨。",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 1,
        },
        {
          mission_id:3,
          title: "【提问】如何设计任务优先级排序算法？",
          tiny_content: "在任务管理系统中，需要根据用户需求动态调整任务的优先级排序。请问有哪些常用的排序算法或者设计思路适合这种场景？",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 2,
        },
        {
          mission_id:3,
          title: "【求助】移动端页面适配问题",
          tiny_content: "项目的移动端页面在不同分辨率设备上显示效果不一致。请问有什么最佳实践或者工具可以帮助解决适配问题？",
          created_at: "2021-09-01",
          created_by: {
            username: "张三",
          },
          tags: ["计算机组成", "2024-2025", "复习资料"],
          commission: 0,
        },
      ],
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
    onCardMouseLeave() {
      if (this.filtersChanged) {
        // 如果 filters 有变化，就重新获取数据
        this.getTasks();
        this.filtersChanged = false; // 重置变化标记
      }
    },
    setFilter(type, value) {
      this.filters[type] = value;
    },
    getTasks() {
      this.loading = false;
    },
    getTagColor(tag) {
      return this.filters.tags.includes(tag) ? 'brown' : 'blue accent-2';
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
    deleteItem(item) {
      // todo 删除操作逻辑
    },
  },
  mounted() {
    this.$store.commit("setAppTitle", "共享资源站");
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
  z-index: 1111; /* 确保按钮位于其他元素之上 */
}
.action-buttons v-btn {
  margin-left: 4px; /* 如果需要按钮之间留白 */
  width: 40px;
  height: 40px;
}

.container {
  padding: 20px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.card {
  position: relative; /* 确保 .action-buttons 以 card 为参考定位 */
  flex: 0 0 48%;
  /* 每行展示三个卡片 */
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #fff;
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

.card-body {
  margin-bottom: 10px;
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
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.author {
  font-size: 14px;
  color: #333;
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