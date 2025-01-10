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
                        <div class=" filters">
                        <v-row class="align-center">
                            <v-col cols="auto">
                                <span><strong>排序</strong>:</span>
                            </v-col>
                            <v-col>
                                <span @click="setFilter('sort_by', 0)"
                                    :class="{ active: filters.sort_by === 0 }">综合</span>
                                <span @click="setFilter('sort_by', 1)"
                                    :class="{ active: filters.sort_by === 1 }">最多点赞</span>
                                <span @click="setFilter('sort_by', 4)"
                                    :class="{ active: filters.sort_by === 4 }">最多收藏</span>
                                <span @click="setFilter('sort_by', 2)"
                                    :class="{ active: filters.sort_by === 2 }">最近创建</span>
                                <span @click="setFilter('sort_by', 3)"
                                    :class="{ active: filters.sort_by === 3 }">最近评论</span>
                            </v-col>
                        </v-row>
                        <v-row class="align-center">
                            <v-col cols="auto">
                                <span><strong>收费</strong>:</span>
                            </v-col>
                            <v-col>
                                <v-radio-group v-model="filters.pay" row>
                                    <v-radio label="不限" :value="0"></v-radio>
                                    <v-radio label="收费" :value="1"></v-radio>
                                    <v-radio label="免费" :value="2"></v-radio>
                                </v-radio-group>
                            </v-col>
                        </v-row>
                        <v-row class="align-center">
                            <v-col cols="auto">
                                <span><strong>标签筛选</strong>:</span>
                            </v-col>
                            <v-col>
                                <v-chip-group v-model="filters.tags" multiple column active-class="active-tag">
                                    <v-chip v-for="(tag, index) in availableTags" :key="index" :color="getTagColor(tag)"
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
                <v-text-field v-model="filters.search" label="请输入搜索内容" placeholder="" filled append-icon="mdi-magnify"
                    hide-details></v-text-field>
            </v-col>
        </v-row>
        </v-card>
    </v-container>
    <v-container>
        <v-row v-for="(item) in post" :key="item.post_id">
            <v-col>
                <div class="card-container">
                    <!-- 卡片主体 -->
                    <v-card outlined class="card-content" style="cursor: pointer;">
                        <v-row no-gutters class="picture">
                            <v-col cols="auto" class="d-flex align-center">
                                <!-- <v-img :src="item.image" aspect-ratio="1" height="110px" width="110px"
                                                contain></v-img> -->
                                <v-icon color="#FFB300"
                                    style="font-size: 106px; margin-left: -10%; margin-right: -20px;">mdi-file-download-outline</v-icon>
                            </v-col>
                            <v-col>
                                <v-card-title>
                                    {{ item.title }}
                                    <v-icon v-if="item.cost > 0" color="#F8CC00">mdi-bitcoin</v-icon>
                                    <span v-if="item.cost > 0"
                                        style="font-size: 13px; color: #666666; margin-left: 0.2%;">
                                        {{ item.cost }} 菜币
                                    </span>
                                </v-card-title>
                                <div style="margin-left: 1.8%;">
                                    <v-chip v-for="(tag, tagIndex) in item.tags" :key="tagIndex" color="aqua" label
                                        small class="me-3">
                                        {{ tag }}
                                    </v-chip>
                                </div>
                                <v-card-actions style="margin-left: 0.8%;">
                                    <div>
                                        <span>
                                            <v-icon
                                                style="display: inline-block; margin-top: -7px;">mdi-thumb-up</v-icon>
                                            <span class="ml-2">{{ item.likes }}</span>
                                        </span>
                                        <span>
                                            <v-icon>mdi-thumb-down</v-icon>
                                            <span class="ml-2">{{ item.dislikes }}</span>
                                        </span>
                                        <span>
                                            <v-icon>mdi-heart-box</v-icon>
                                            <span class="ml-2">{{ item.favorites }}</span>
                                        </span>
                                        <span>
                                            <v-icon>mdi-comment-multiple</v-icon>
                                            <span class="ml-2">{{ item.comments }}</span>
                                        </span>
                                    </div>
                                    <div class="ml-auto">
                                        <span>{{ item.author }}</span>
                                        <span>{{ item.date }}</span>
                                    </div>
                                </v-card-actions>
                            </v-col>
                        </v-row>
                    </v-card>
                    <!-- 操作按钮 -->
                    <div class="action-buttons">
                        <v-btn color="primary" class="me-2" icon @click.stop="openItem(item.link)">
                            <v-icon style="font-size: 32px;">mdi-open-in-new</v-icon>
                        </v-btn>
                        <v-btn color="red" icon @click.stop="deleteItem(item)">
                            <v-icon style="font-size: 32px;">mdi-delete</v-icon>
                        </v-btn>
                    </div>
                </div>
            </v-col>
        </v-row>
    </v-container>

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
                tags: [],
                search: ''
            },
            availableTags: [
                "计算机组成", "数据库", "面向对象", "测试", "考试题", "数据结构", "2023-2024", "2024-2025", "复习资料"
            ],
            filtersChanged: false, // 用来标记 filters 是否有变化
            post: [
                {
                    post_id: 1,
                    link: "/resources/testPost", // todo 链接
                    image: require("@/assets/images/blogDefault.png"), // 这里需要申请另一个api
                    title: "计算机组成考试题（2023-2024学年）",
                    icon: { name: "mdi-bitcoin", color: "#F8CC00" },
                    cost: 5,
                    tags: ["计算机组成", "考试题", "2023-2024"], // 这里需要申请另一个api
                    likes: 3407,
                    dislikes: 109,
                    favorites: 96,
                    comments: 12,
                    created_by: {
                        user_id: 1,
                        username: "张三",
                        avatar: require("@/assets/images/blogDefault.png"),
                    },
                    created_at: "2024-04-29",
                },
                {
                    post_id: 2,
                    link: "/resources/testPost",
                    title: "数据结构期末复习资料（2024-2025学年）",
                    subtitle: "这是一份数据结构的复习资料，涵盖了本学年考试的重点知识点。希望对大家有所帮助。",
                    tags: ["数据结构", "复习资料", "2024-2025"],
                    cost: 0,
                    likes: 5289,
                    dislikes: 143,
                    favorites: 305,
                    comments: 25, // 这里需要获取帖子的评论数量
                    created_by: {
                        user_id: 2,
                        username: "李四",
                        avatar: require("@/assets/images/blogDefault.png"),
                    },
                    created_at: "2024-05-10",
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
                this.getPosts();
                this.filtersChanged = false; // 重置变化标记
            }
        },
        setFilter(type, value) {
            this.filters[type] = value;
        },
        getPosts() {
            // 获取数据
            this.$store.dispatch("getPosts", { pay: this.filters.pay, sort_by: this.filters.sort_by, search: this.filters.search })
                .then(res => {
                    this.posts = res.posts;
                })
                .catch(_ => {
                    this.posts = [];
                    this.$store.commit("setAlert", { type: "error", message: "无法连接到资源站。请检查你的网络设置。" })
                })
                .finally(() => {
                    this.loading = false;
                });
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
        goToPage(page) {
            this.$router.push(page);
        },
        openItem(link) {
            // todo 打开操作逻辑
            this.goToPage(link);
        },
        deleteItem(item) {
            // todo 删除操作逻辑
        },
    },
    mounted() {
        this.$store.commit("setAppTitle", "管理资源");
        this.getPosts();
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
    background: #d9fe32;
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
    top: 30px;
    right: 20px;
    display: flex;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.card-container:hover .action-buttons {
    opacity: 1;
    /* 鼠标悬浮时显示按钮 */
}
</style>