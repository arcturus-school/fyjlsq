import {
  UserOutlined,
  LockOutlined,
  PlusOutlined,
  LoadingOutlined,
  ArrowLeftOutlined,
  InboxOutlined,
} from '@ant-design/icons-vue';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

import {
  faBold,
  faRotateRight,
  faRotateLeft,
  faItalic,
  faUnderline,
  faStrikethrough,
  faAlignCenter,
  faAlignRight,
  faAlignLeft,
  faAlignJustify,
  faFillDrip,
  faA,
  faListUl,
  faListOl,
  faImage,
  faSquareCheck,
  faPaperclip,
  faQuoteLeft,
  faGripLines,
  faCaretDown,
  faTrash,
  faShareNodes,
  faPenToSquare,
  faArrowLeft,
} from '@fortawesome/free-solid-svg-icons';

export default {
  install(app) {
    // 注册 ant-design 图标
    app
      .component('user-outlined', UserOutlined)
      .component('lock-outlined', LockOutlined)
      .component('loading-outlined', LoadingOutlined)
      .component('arrow-left-outlined', ArrowLeftOutlined)
      .component('plus-outlined', PlusOutlined)
      .component('inbox-outlined', InboxOutlined);

    // 注册 fontawesome 图标
    library.add(
      faBold,
      faRotateRight,
      faRotateLeft,
      faItalic,
      faUnderline,
      faStrikethrough,
      faAlignCenter,
      faAlignRight,
      faAlignLeft,
      faAlignJustify,
      faFillDrip,
      faListUl,
      faListOl,
      faA,
      faImage,
      faSquareCheck,
      faPaperclip,
      faQuoteLeft,
      faGripLines,
      faCaretDown,
      faArrowLeft,
      faTrash,
      faShareNodes,
      faPenToSquare
    );

    app.component('font-awesome-icon', FontAwesomeIcon);
  },
};
