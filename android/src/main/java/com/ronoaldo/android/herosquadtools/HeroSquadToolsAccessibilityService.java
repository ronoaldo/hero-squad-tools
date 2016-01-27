package com.ronoaldo.android.herosquadtools;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.util.Log;

public class HeroSquadToolsAccessibilityService extends AccessibilityService {

	public static final String TAG = "HeroSquadTools";

	@Override
	public void onAccessibilityEvent(AccessibilityEvent event) {
		Log.v(TAG, "New event received: " + event.toString());
		Log.v(TAG, "Root in active window: " + this.getRootInActiveWindow());
	}

	@Override
	public void onInterrupt() {
		Log.v(TAG, "Service interrupted!");
	}
}
