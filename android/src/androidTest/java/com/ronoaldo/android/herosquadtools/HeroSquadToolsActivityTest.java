package com.ronoaldo.android.herosquadtools;

import android.test.ActivityInstrumentationTestCase2;

/**
 * This is a simple framework for a test of an Application.  See
 * {@link android.test.ApplicationTestCase ApplicationTestCase} for more information on
 * how to write and extend Application tests.
 * <p/>
 * To run this test, you can type:
 * adb shell am instrument -w \
 * -e class com.ronoaldo.android.herosquadtools.HeroSquadToolsActivityTest \
 * com.ronoaldo.android.herosquadtools.tests/android.test.InstrumentationTestRunner
 */
public class HeroSquadToolsActivityTest extends ActivityInstrumentationTestCase2<HeroSquadToolsActivity> {

    public HeroSquadToolsActivityTest() {
        super("com.ronoaldo.android.herosquadtools", HeroSquadToolsActivity.class);
    }

}
