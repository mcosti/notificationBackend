# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from os import wait
from time import sleep

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from yeelight import *

color_dict = {
    "com.facebook.katana" : (59,89,152),
    "com.facebook.orca" : (0, 204, 102),
    "com.whatsapp" : (153, 255, 204),
    "com.instagram.android": (204, 102, 0),
    "com.google.android.gm" : (255, 0, 0)
}


def notification_pulse(device, color):
    #device.start_music()
    status = device.get_properties()['power']
    device.effect="smooth"
    device.turn_on()
    device.set_brightness(75)
    device.set_rgb(color[0], color[1], color[2])
    sleep(1)
    device.turn_off()
    sleep(1)
    device.turn_on()
    sleep(1)
    #device.turn_off()
    #sleep(1)
    #device.turn_on()
    if status ==  u'off':
        device.turn_off()
    return status



@csrf_exempt
def index(request):

    auth_key = "123" #getattr(settings, "auth_key", None)
    if request.POST.get('auth_key') != auth_key:
        r = {
            'error' : "Auth key invalid",
            'sent_auth' : request.POST.get('auth_key')
        }
        return JsonResponse(r)

    else:
        package = request.POST.get('package')
        if package:
            color = color_dict[package]
            device_ip = "192.168.100.12" #getattr(settings, "device_ip", None)
            try:
                device = Bulb(device_ip)
            except BulbException:
                return HttpResponse("Couldn't get device")
            status = notification_pulse(device, color)
            return HttpResponse("Status is: ", status)

        else:
            return HttpResponse("No package posted")


