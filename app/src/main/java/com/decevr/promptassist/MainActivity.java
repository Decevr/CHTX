package com.decevr.promptassist;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Toast;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        setContentView(web);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        web.addJavascriptInterface(new Bridge(), "PromptAssist");
        web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    public void onBackPressed() {
        if (web == null) {
            super.onBackPressed();
            return;
        }
        web.evaluateJavascript(
                "(function(){var d=document.getElementById('detail');if(d&&!d.hidden){d.hidden=true;d.innerHTML='';return 'closed';}return '';})()",
                value -> {
                    if (value == null || !value.contains("closed")) {
                        MainActivity.super.onBackPressed();
                    }
                }
        );
    }

    private class Bridge {
        @JavascriptInterface
        public void copy(String text) {
            runOnUiThread(() -> {
                ClipboardManager clipboard = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
                clipboard.setPrimaryClip(ClipData.newPlainText("prompt", text));
                Toast.makeText(MainActivity.this, "Copied", Toast.LENGTH_SHORT).show();
            });
        }
    }
}
