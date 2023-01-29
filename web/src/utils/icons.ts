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
  faLeftLong,
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
  faPlus,
  faUser,
  faLock,
} from '@fortawesome/free-solid-svg-icons';
import { App } from 'vue';

export default {
  install(app: App) {
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
      faPenToSquare,
      faPlus,
      faUser,
      faLock,
      faLeftLong
    );

    app.component('font-awesome-icon', FontAwesomeIcon);
  },
};
