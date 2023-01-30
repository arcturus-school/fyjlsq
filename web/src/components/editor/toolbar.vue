<template>
  <a-row class="style-toolbar-container" justify="center">
    <a-space style="position: relative">
      <!-- 撤销 -->
      <a-tooltip placement="bottom">
        <template #title> 撤销 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-disabled': !props.editor?.can().undo(),
          }"
          @click="props.editor?.commands.undo()"
        >
          <font-awesome-icon icon="fa-solid fa-rotate-left" size="lg" />
        </div>
      </a-tooltip>

      <!-- 重做 -->
      <a-tooltip placement="bottom">
        <template #title> 重做 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-disabled': !props.editor?.can().redo(),
          }"
          @click="props.editor?.commands.redo()"
        >
          <font-awesome-icon icon="fa-solid fa-rotate-right" size="lg" />
        </div>
      </a-tooltip>

      <!-- 正文与标题 -->
      <a-select
        v-model:value="defaultTextType"
        style="width: 90px"
        dropdownClassName="style-select-dropdown"
        :dropdownMatchSelectWidth="false"
        optionLabelProp="label"
        @change="toggleHeader"
      >
        <a-select-option
          v-for="item in textTypes"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          style="line-height: 2.4em; padding: 0 12px"
        >
          <component :is="item.vNode"></component>
        </a-select-option>

        <!-- 下拉图标 -->
        <template #suffixIcon>
          <font-awesome-icon icon="fa-solid fa-caret-down" size="lg" />
        </template>
      </a-select>

      <!-- 加粗 -->
      <a-tooltip placement="bottom">
        <template #title> 加粗 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('bold'),
          }"
          @click="props.editor?.commands.toggleBold()"
        >
          <font-awesome-icon icon="fa-solid fa-bold" size="lg" />
        </div>
      </a-tooltip>

      <!-- 斜体 -->
      <a-tooltip placement="bottom">
        <template #title> 斜体 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('italic'),
          }"
          @click="props.editor?.commands.toggleItalic()"
        >
          <font-awesome-icon icon="fa-solid fa-italic" size="lg" />
        </div>
      </a-tooltip>

      <!-- 下划线 -->
      <a-tooltip placement="bottom">
        <template #title> 下划线 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('underline'),
          }"
          @click="props.editor?.commands.toggleUnderline()"
        >
          <font-awesome-icon icon="fa-solid fa-underline" size="lg" />
        </div>
      </a-tooltip>

      <!-- 删除线 -->
      <a-tooltip placement="bottom">
        <template #title> 删除线 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('strike'),
          }"
          @click="props.editor?.commands.toggleStrike()"
        >
          <font-awesome-icon icon="fa-solid fa-strikethrough" size="lg" />
        </div>
      </a-tooltip>

      <Divider type="vertical"></Divider>

      <!-- 字体颜色 -->
      <a-tooltip placement="bottom">
        <template #title> 字体颜色 </template>

        <a-popover
          placement="bottom"
          trigger="click"
          :visible="textColorPickerVisible"
          @visibleChange="handleTextColorPickerClick"
        >
          <template #content>
            <!-- 拾色器 -->
            <ColorPicker
              class="style-color-picker"
              theme="light"
              :color="TextColor"
              :sucker-hide="true"
              @changeColor="changeTextColor"
            />
          </template>
          <div class="style-toolbar-btn">
            <font-awesome-icon icon="fa-solid fa-a" size="lg" />
            <div
              class="style-a-color"
              :style="{
                backgroundColor:
                  props.editor?.getAttributes('textStyle').color ?? '#000',
              }"
            ></div>
          </div>
        </a-popover>
      </a-tooltip>

      <!-- 背景颜色 -->
      <a-tooltip placement="bottom">
        <template #title> 背景颜色 </template>

        <a-popover
          placement="bottom"
          trigger="click"
          :visible="textBackgroundColorPickerVisible"
          @visibleChange="handleTextBackgroundColorPickerClick"
        >
          <template #content>
            <!-- 拾色器 -->
            <ColorPicker
              class="style-color-picker"
              theme="light"
              :color="TextBackgroundColor"
              :sucker-hide="true"
              @changeColor="changeTextBackgroundColor"
            />
          </template>
          <div class="style-toolbar-btn">
            <font-awesome-icon icon="fa-solid fa-fill-drip" />
            <div
              class="style-a-color"
              :style="{
                backgroundColor:
                  props.editor?.getAttributes('highlight').color ?? '#fff',
              }"
            ></div>
          </div>
        </a-popover>
      </a-tooltip>

      <Divider type="vertical"></Divider>

      <!-- 对齐方式 -->
      <a-select
        v-model:value="defaultAlignMethod"
        style="width: 60px"
        class="style-toolbar-btn"
        :dropdownMatchSelectWidth="false"
        optionLabelProp="vNode"
        @change="toggleAlign"
      >
        <a-select-option
          v-for="item in alginMethods"
          :vNode="item.vNode"
          :key="item.value"
        >
          <a-space>
            <component :is="item.vNode"></component>
            <div>{{ item.label }}</div>
          </a-space>
        </a-select-option>

        <template #suffixIcon>
          <font-awesome-icon icon="fa-solid fa-caret-down" size="lg" />
        </template>
      </a-select>

      <!-- 无序序列 -->
      <a-tooltip placement="bottom">
        <template #title> 无序序列 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('bulletList'),
          }"
          @click="props.editor?.commands.toggleBulletList()"
        >
          <font-awesome-icon icon="fa-solid fa-list-ul" size="lg" />
        </div>
      </a-tooltip>

      <!-- 有序序列 -->
      <a-tooltip placement="bottom">
        <template #title> 有序序列 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('orderedList'),
          }"
          @click="props.editor?.commands.toggleOrderedList()"
        >
          <font-awesome-icon icon="fa-solid fa-list-ol" size="lg" />
        </div>
      </a-tooltip>

      <Divider type="vertical"></Divider>

      <!-- 任务 -->
      <a-tooltip placement="bottom">
        <template #title> 任务列表 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('taskList'),
          }"
          @click="props.editor?.commands.toggleTaskList()"
        >
          <font-awesome-icon icon="fa-solid fa-square-check" size="lg" />
        </div>
      </a-tooltip>

      <!-- 图片 -->
      <a-tooltip placement="bottom">
        <template #title> 插入图片 </template>
        <div class="style-toolbar-btn" @click="openUploadModal">
          <font-awesome-icon icon="fa-solid fa-image" size="lg" />
        </div>

        <a-modal v-model:visible="uploadImageVisible" title="上传图片">
          <a-upload
            v-model:fileList="ImageList"
            name="source"
            accept="image/*"
            list-type="picture-card"
            action="/upload"
            :headers="headers"
            :show-upload-list="false"
            class="style-image-uploader"
            @change="handleImageUploadChange"
          >
            <div
              v-if="imageLink"
              :style="{
                width: '100%',
                height: '100%',
                background: `url(${imageLink})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
              }"
            />
            <div v-else>
              <a-spin v-if="uploadLoading" />
              <font-awesome-icon icon="fa-solid fa-plus" v-else />
            </div>
          </a-upload>

          <template #footer>
            <a-button
              type="primary"
              @click="insertImage"
              :disabled="canNotInsertImage"
            >
              插入
            </a-button>
          </template>
        </a-modal>
      </a-tooltip>

      <!-- 链接 -->
      <a-tooltip placement="bottom">
        <template #title> 插入链接 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('link'),
          }"
          @click="openLinkModal"
        >
          <font-awesome-icon icon="fa-solid fa-paperclip" size="lg" />
        </div>

        <a-modal
          v-model:visible="linkEditorVisible"
          title="插入链接"
          @ok="addLink"
          okText="插入"
          @cancel="deleteLink"
          cancelText="删除"
        >
          <a-input v-model:value="link" />
        </a-modal>
      </a-tooltip>

      <!-- 引用 -->
      <a-tooltip placement="bottom">
        <template #title> 插入引用 </template>
        <div
          class="style-toolbar-btn"
          :class="{
            'is-active': props.editor?.isActive('blockquote'),
          }"
          @click="props.editor?.commands.toggleBlockquote()"
        >
          <font-awesome-icon icon="fa-solid fa-quote-left" size="lg" />
        </div>
      </a-tooltip>

      <!-- 分段 -->
      <a-tooltip placement="bottom">
        <template #title> 插入分割线 </template>
        <div
          class="style-toolbar-btn"
          @click="props.editor?.commands.setHorizontalRule()"
        >
          <font-awesome-icon icon="fa-solid fa-grip-lines" size="lg" />
        </div>
      </a-tooltip>
    </a-space>
  </a-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { log } from '@utils/log';

export default defineComponent({
  name: 'toolbar',
  components: { Divider },
});
</script>

<script setup lang="ts">
import { h, ref, computed } from 'vue';
import { Editor } from '@tiptap/vue-3';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { Divider, message } from 'ant-design-vue';
import type { UploadChangeParam, UploadProps } from 'ant-design-vue';
import { getImageName, getImageUrl, headers } from '@src/image';
// 拾色器
import { ColorPicker } from 'vue-color-kit';
import 'vue-color-kit/dist/vue-color-kit.css';

const props = defineProps({
  editor: {
    type: Editor,
  },
});

const textTypes = ref([
  {
    value: 1,
    label: '标题一',
    vNode: h('h1', '标题一'),
  },
  {
    value: 2,
    label: '标题二',
    vNode: h('h2', '标题二'),
  },
  {
    value: 3,
    label: '标题三',
    vNode: h('h3', '标题三'),
  },
  {
    value: 4,
    label: '标题四',
    vNode: h('h4', '标题四'),
  },
  {
    value: 5,
    label: '标题五',
    vNode: h('h5', '标题五'),
  },
  {
    value: 6,
    label: '标题六',
    vNode: h('h6', '标题六'),
  },
  {
    value: 0,
    label: '正文',
    vNode: h('text', '正文'),
  },
]);

const defaultTextType = ref(0);

const alginMethods = ref([
  {
    value: 'left',
    label: '左对齐',
    vNode: h(FontAwesomeIcon, {
      icon: 'fa-solid fa-align-left',
      size: 'lg',
    }),
  },
  {
    value: 'right',
    label: '右对齐',
    vNode: h(FontAwesomeIcon, {
      icon: 'fa-solid fa-align-right',
      size: 'lg',
    }),
  },
  {
    value: 'center',
    label: '居中',
    vNode: h(FontAwesomeIcon, {
      icon: 'fa-solid fa-align-center',
      size: 'lg',
    }),
  },
  {
    value: 'justify',
    label: '两端对齐',
    vNode: h(FontAwesomeIcon, {
      icon: 'fa-solid fa-align-justify',
      size: 'lg',
    }),
  },
]);

const defaultAlignMethod = ref('left');

// 设置标题样式
function toggleHeader(e: any) {
  if ([1, 2, 3, 4, 5, 6].includes(e)) {
    props.editor?.commands.setHeading({ level: e as any });
  } else {
    // 文本恢复默认样式
    props.editor?.commands.unsetAllMarks();
    props.editor?.commands.clearNodes();
  }
}

// 设置水平居中方式
function toggleAlign(e: any) {
  props.editor?.commands.setTextAlign(e);
}

// 颜色相关

// 文本颜色
const TextColor = ref('#000');
const textColorPickerVisible = ref(false);

function handleTextColorPickerClick(vis: boolean) {
  textColorPickerVisible.value = vis;
}

// 设置文本颜色
function changeTextColor(color: Color) {
  props.editor?.commands.setColor(color.hex);
}

// 背景颜色
const TextBackgroundColor = ref('#000');
const textBackgroundColorPickerVisible = ref(false);

function handleTextBackgroundColorPickerClick(vis: boolean) {
  textBackgroundColorPickerVisible.value = vis;
}

// 设置文本颜色
function changeTextBackgroundColor(color: Color) {
  props.editor?.commands.setHighlight({ color: color.hex });
}

const linkEditorVisible = ref(false);

const link = ref('');

function openLinkModal() {
  if (
    props.editor?.isActive('link') &&
    typeof props.editor.getAttributes('link').href !== 'undefined'
  ) {
    link.value = props.editor.getAttributes('link').href;
  } else {
    link.value = '';
  }

  linkEditorVisible.value = true;
}

function addLink() {
  props.editor?.commands.setLink({
    href: link.value,
    target: '_blank',
  });

  linkEditorVisible.value = false;
}

function deleteLink() {
  if (props.editor?.isActive('link')) {
    props.editor?.commands.unsetLink();
  }

  linkEditorVisible.value = false;
}

// 图片上传相关
const uploadImageVisible = ref(false);
const imageLink = ref('');
const uploadLoading = ref(false);
const ImageList = ref<UploadProps['fileList']>([]);

const canNotInsertImage = computed(() => imageLink.value === '');

function openUploadModal() {
  imageLink.value !== '';
  uploadImageVisible.value = true;
}

// 图片上传
function handleImageUploadChange(info: UploadChangeParam) {
  const status = info.file.status;

  if (status === 'uploading') {
    uploadLoading.value = true;
  } else if (status === 'done') {
    const idx = ImageList.value!.length - 1;

    log(ImageList.value![idx]);

    imageLink.value = getImageUrl(ImageList.value![idx].response);
    uploadLoading.value = false;
  } else if (status === 'error') {
    message.error('图片上传失败');
    uploadLoading.value = false;
  }
}

// 编辑器中插入图片
function insertImage() {
  if (imageLink.value !== '') {
    const idx = ImageList.value!.length - 1;

    props.editor?.commands.setImage({
      src: getImageUrl(ImageList.value![idx].response),
      alt: getImageName(ImageList.value![idx].response),
    });
  }

  uploadImageVisible.value = false;
  ImageList.value!.length = 0;
  imageLink.value = '';
}
</script>

<style scoped>
.style-toolbar-container {
  position: sticky;
  background-color: #fafafa;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 20px;
  width: 100%;
  height: 56px;
  left: 0;
  top: 0;
  z-index: 999;
}

.style-toolbar-btn {
  cursor: pointer;
  width: 30px;
  height: 30px;
  text-align: center;
  line-height: 30px;
  border-radius: 6px;
}

.style-toolbar-btn:hover {
  background-color: #f4f5f5;
}

.style-toolbar-btn.is-active {
  background-color: #e7e9e8;
}

.style-toolbar-btn.is-disabled {
  pointer-events: none;
  opacity: 0.4;
}

:global(.style-select-dropdown :is(h1, h2, h3, h4, h5, h6)) {
  margin-bottom: 0 !important;
}

:deep(.ant-select .ant-select-selector) {
  background-color: transparent !important;
  border: none !important;
}

:deep(.ant-select-focused .ant-select-selector) {
  box-shadow: none !important;
}

:global(.style-select-dropdown .rc-virtual-list-holder) {
  max-height: fit-content !important;
}

/* 字体颜色 */
.style-a-color {
  height: 2px;
  width: 15px;
  border-radius: 2px;
  transform: translate(50%, -300%);
}

.style-color-picker {
  background: transparent;
  box-shadow: none;
  padding: 0;
}

:deep(.style-image-upload-dragger) {
  height: 200px !important;
}

:deep(.style-image-upload-dragger .ant-upload-btn) {
  display: flex !important;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

:global(.style-image-uploader) {
  height: 200px;
}

:global(.style-image-uploader > .ant-upload) {
  height: 100% !important;
  width: 100% !important;
}
</style>
