<template>
  <a-form
    class="style-form-container"
    :model="formState"
    :label-col="{ span: 4 }"
    :wrapper-col="{ span: 20 }"
    @finish="onFinish"
  >
    <!-- 工具栏 -->
    <Toolbar :editor="editor"></Toolbar>

    <div class="style-edit-wrap">
      <!-- 富文本编辑器 -->
      <div class="style-editor-content">
        <editor-content :editor="editor" />
      </div>

      <!-- 发布设置 -->
      <div class="style-form-wrap">
        <a-form-item
          label="标题设置"
          name="title"
          labelAlign="left"
          :rules="[
            {
              required: true,
              message: '请输入标题',
            },
          ]"
        >
          <!-- 标题输入框 -->
          <a-input v-model:value="formState.title" />
        </a-form-item>

        <a-form-item
          label="文章摘要"
          name="title"
          labelAlign="left"
          :rules="[
            {
              required: true,
              message: '请输入摘要',
            },
          ]"
        >
          <!-- 文章摘要 -->
          <a-textarea
            v-model:value="formState.abstract"
            showCount
            :maxlength="100"
          />
        </a-form-item>

        <a-form-item
          label="展示封面"
          name="cover"
          labelAlign="left"
          :rules="[
            {
              required: true,
              message: '请上传封面',
            },
          ]"
        >
          <!-- 上传组件 -->
          <a-upload
            v-model:file-list="formState.cover"
            name="file"
            list-type="picture-card"
            accept="image/*"
            class="style-cover-uploader"
            :show-upload-list="false"
            :action="IMAGE_UPLOAD_URL"
            :before-upload="beforeUpload"
            @change="handleChange"
          >
            <div
              v-if="imageUrl"
              :style="{
                width: '100%',
                height: '100%',
                background: `url(${imageUrl})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }"
            />
            <div v-else>
              <!-- 加载图标 -->
              <loading-outlined v-if="loading" />
              <!-- 添加图标 -->
              <plus-outlined v-else />
            </div>
          </a-upload>
        </a-form-item>
      </div>

      <!-- 底部工具栏 -->
      <div class="style-publish-footer">
        <div class="style-publish-footer-content">
          <div class="style-footer-tip">
            共 {{ characters }} 字
          </div>

          <a-button type="primary" html-type="submit">
            发布
          </a-button>
        </div>
      </div>
    </div>
  </a-form>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'editor',
});
</script>

<script setup>
import {
  ref,
  reactive,
  computed,
  defineProps,
  onMounted,
} from 'vue';
import { getBase64 } from '@utils/handle';
import { message } from 'ant-design-vue';
import { IMAGE_UPLOAD_URL } from '@/config';

import { useRouter } from 'vue-router';
import { useArticle } from '@/store';

// 富文本编辑器
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import CharacterCount from '@tiptap/extension-character-count';
import Placeholder from '@tiptap/extension-placeholder';
import Underline from '@tiptap/extension-underline';
import TaskItem from '@tiptap/extension-task-item';
import TaskList from '@tiptap/extension-task-list';
import TextAlign from '@tiptap/extension-text-align';
import TextStyle from '@tiptap/extension-text-style';
import Highlight from '@tiptap/extension-highlight';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import { Color } from '@tiptap/extension-color';

import Toolbar from '@/components/editor/toolbar.vue';

const props = defineProps({
  articleInfo: Object,
});

// tiptap
const editor = useEditor({
  content: '',
  extensions: [
    // 添加 tiptap 扩展
    StarterKit.configure({
      heading: {
        HTMLAttributes: {
          class: 'style-heading-class',
        },
      },
      horizontalRule: {
        HTMLAttributes: {
          class: 'style-hr-class',
        },
      },
      history: {
        depth: 20,
      },
    }),
    TextAlign.configure({
      defaultAlignment: 'left',
      types: ['heading', 'paragraph'],
    }),
    TaskItem.configure({
      nested: true,
    }),
    Highlight.configure({
      multicolor: true,
      HTMLAttributes: {
        class: 'style-hightline-class',
      },
    }),
    Link,
    TaskList,
    Image,
    TextStyle,
    Color,
    CharacterCount,
    Underline,
    Placeholder.configure({
      placeholder: ({ node }) => {
        if (node.type.name === 'heading') {
          return '输入标题';
        }

        return '请输入正文';
      },
    }),
  ],
});

// 编辑器的字符数
const characters = computed(() => {
  return (
    editor.value?.storage.characterCount.characters() ?? 0
  );
});

const article = useArticle();
const router = useRouter();

const formState = reactive({
  title: '',
  cover: [],
  count: 0,
  abstract: '',
});

const loading = ref(false);
const imageUrl = ref('');

onMounted(() => {
  const { articleInfo } = props;
  if (articleInfo !== null) {
    formState.title = articleInfo.title;
    formState.cover = [articleInfo.cover];
    imageUrl.value = articleInfo.cover;
    formState.abstract = articleInfo.abstract;
    editor.value?.commands.insertContent(
      articleInfo.content
    );
  }
});

// 上传图片前操作
function beforeUpload(file) {
  const isJpgOrPng =
    file.type === 'image/jpeg' || file.type === 'image/png';

  if (!isJpgOrPng) {
    message.error('仅支持 jpg 与 png');
  }

  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isLt2M) {
    message.error('图片必须小于 2M');
  }

  return isJpgOrPng && isLt2M;
}

// 上传文件改变时的状态
function handleChange(info) {
  if (info.file.status === 'uploading') {
    imageUrl.value = '';
    loading.value = true;
  } else if (info.file.status === 'done') {
    const idx = formState.cover.length - 1;

    imageUrl.value =
      formState.cover[idx].response.data.links.url;
    loading.value = false;
  } else if (info.file.status === 'error') {
    message.error('封面图上传失败');
    loading.value = false;
  }
}

// 数据提交
function onFinish() {
  const data = {
    content: editor.value.getHTML(),
    title: formState.title,
    cover: imageUrl.value,
    characters: characters.value,
    abstract: formState.abstract,
  };

  if (props.articleInfo !== null) {
    data.id = props.articleInfo.id;

    article.edit(data).then((res) => {
      if (res) {
        // 跳转至文章页面
        router.push({
          path: `/article-detail/${props.articleInfo.id}`,
        });
      }
    });
  } else {
    article.post(data).then((id) => {
      if (id) {
        // 跳转至文章页面
        router.push({ path: `/article-detail/${id}` });
      }
    });
  }
}
</script>

<style scoped>
.style-edit-wrap {
  position: relative;
  border-radius: 2px;
  background-color: #fff;
  width: 816px;
  margin: 20px auto 100px;
}

.style-editor-content {
  padding: 48px 0;
  margin: 0 64px;
}

.style-form-wrap {
  padding: 48px 0 12px;
  margin: 0 64px;
  border-top: 1px solid #e8e8e8;
}

.style-publish-footer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 68px;
  width: 100vw;
  line-height: 68px;
  z-index: 10;
  background-color: #fff;
  border-top: 1px solid #e8e8e8;
  text-align: right;
}

.style-publish-footer-content {
  height: 100%;
  width: 816px;
  margin: 0 auto;
}

.style-footer-tip {
  font-size: 12px;
  color: #666;
  float: left;
  height: 100%;
  vertical-align: middle;
  line-height: 68px;
}

:deep(.style-cover-uploader > .ant-upload) {
  width: 256px;
  height: 144px;
}

/* placeholder */
:deep(.ProseMirror
    :is(p, h1, h2, h3, h4, h5, h6).is-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}

:deep(.ProseMirror:focus) {
  outline: none;
}

/* 引用样式 */
:deep(.ProseMirror blockquote) {
  padding-left: 0.5rem;
  border-left: 3px solid #e0e0e0;
}

/* 普通列表 */
:deep(ul) {
  padding: 0 0 0 20px;
}

:deep(ol) {
  padding: 0 0 0 20px;
}

/* 任务列表样式 */
:deep(ul[data-type='taskList']) {
  list-style: none;
  padding: 0;
}

:deep(ul[data-type='taskList'] li) {
  display: flex;
}

:deep(ul[data-type='taskList'] p) {
  margin: 0;
}

:deep(ul[data-type='taskList'] li label) {
  flex: 0 0 auto;
  margin-right: 0.5rem;
  display: flex;
  align-items: center;
  user-select: none;
}

:deep(ul[data-type='taskList'] li div) {
  flex: 1 1 auto;
  line-height: 1.5em;
  height: 1.5em;
}

/* 自定义 heading 样式 */
:deep(.style-heading-class) {
  font-weight: bold;
}

/* 水平线样式 */
:deep(.style-hr-class) {
  height: 2px;
  border: none;
  border-top: 2px dashed #eeeeee;
}

:deep(.style-hightline-class) {
  padding: 0.125em 0.125em;
  margin: 0 0.125em;
  border-radius: 0.25em;
  box-decoration-break: clone;
}

/* 图片样式 */
:deep(.ProseMirror > img) {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
}

:deep(.ProseMirror > img.ProseMirror-selectednode) {
  outline: 3px solid #68cef8;
}
</style>
