from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Conversation, Message
from .paginaters import MessagePagination
from rest_framework.permissions import IsOwnerOrReadOnly
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework import permissions


# Permissions for ConversationViewSet
class IsConversationParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.username in obj.name

class IsConversationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

class ConversationViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"
    permission_classes = [IsOwnerOrReadOnly] # Add this line to enable the permission class
    

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.username
        )
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}

    # Apply permissions for list and retrieve actions
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsConversationParticipant()]
        elif self.action in ["update", "destroy"]:
            return [IsConversationOwner()]
        return []


# Permissions for MessageViewSet
class IsMessageParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.from_user or
            request.user == obj.to_user
        )

class IsMessageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

class MessageViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset
    
    # Apply permissions for list and create actions

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsMessageParticipant()]
        elif self.action in ["update", "destroy"]:
            return [IsMessageOwner()]
        return []