from chats.views import ConversationViewSet, MessageViewSet

router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)