from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from customAdmin.models import All_user,Message as msg
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q

class Message(View):

	def get(self,request,profile_id):
		profile_details = All_user.objects.get(id=profile_id)
		ownId = request.session["loggedInUser"]["id"]
		allMessage = msg.objects.filter(Q(receiver=ownId,sender=profile_id) | Q(receiver=profile_id,sender=ownId)).order_by("-id")
		receiverMsg = msg.objects.filter(sender=profile_id,receiver=ownId)
		if receiverMsg:
			receiverMsg.update(seen=True)
		context = {"receiver":profile_details,"allMessage":allMessage}
		return render(request,"Message/add-message.html",context)


	def post(self,request,profile_id):
		messageBody = request.POST.get("message")
		newMessage = msg(
				sender=All_user.objects.get(id=request.session["loggedInUser"]["id"]),
				receiver=All_user.objects.get(id=profile_id),
				message=messageBody,
			)
		newMessage.save()
		profile_details = All_user.objects.get(id=profile_id)
		ownId = request.session["loggedInUser"]["id"]
		allMessage = msg.objects.filter(Q(receiver=ownId,sender=profile_id) | Q(receiver=profile_id,sender=ownId)).order_by("-id")
		context = {"receiver":profile_details,"allMessage":allMessage}
		return render(request,"Message/view-message.html",context)

	def allMessage(request):
		ownId = request.session["loggedInUser"]["id"]
		profile_details = All_user.objects.get(id=ownId)
		userMessages = msg.objects.filter(Q(receiver=ownId) | Q(sender=ownId)).order_by("-id")
		chatList = []
		for i in userMessages:
			if not i.sender.id == ownId:
				if not i.sender.id in chatList:
					chatList.append(i.sender.id)
			if not i.receiver.id == ownId:
				if not i.receiver.id in chatList:
					chatList.append(i.receiver.id)
		print(chatList)
		context = {"receiver":profile_details,"userMessages":userMessages,"chatList":chatList}
		return render(request,"Message/all-message.html",context)