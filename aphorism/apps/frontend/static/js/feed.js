import {isMe, isSubscribed, subscribe, unsubscribe} from "./actions.js";

const postButton = document.querySelector(".profile_counts_wrapper > .button");

const getCurrentUser = () => {
  const href = window.location.href.split('/');
  const slug = href[href.length - 1];
  return {
    slug,
    isSubscribed: () => isSubscribed(slug),
    subscribe: () => subscribe(slug),
    unsubscribe: () => unsubscribe(slug)
  }
}
const currentUser = getCurrentUser();


function setCreatePostStyle() {}
function createPost() { /* TODO: redirect */ }

function setSubscriptionStyle() {}
async function toggleSubscription() {
  if (await currentUser.isSubscribed()) {
    await currentUser.unsubscribe();
    postButton.textContent = "Subscribe";
  } else {
    await currentUser.subscribe();
    postButton.textContent = "Unsubscribe";
  }
}

const [changeStyle, listener] =
  isMe(currentUserSlug)
    ? [setCreatePostStyle, createPost]
    : [setSubscriptionStyle, toggleSubscription];

changeStyle();
postButton.addEventListener("click", listener);
