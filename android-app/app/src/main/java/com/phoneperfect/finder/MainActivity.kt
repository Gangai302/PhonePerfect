package com.phoneperfect.finder

import android.annotation.SuppressLint
import android.graphics.Color
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : ComponentActivity() {
    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled", "JavascriptInterface")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Android 15+ (targetSdk 35+) forces edge-to-edge – cannot be disabled.
        enableEdgeToEdge()

        // ── Container approach ──────────────────────────────────────────────────
        // The WebView sits inside a FrameLayout that is padded by the status-bar
        // height.  We read the height SYNCHRONOUSLY from Android system resources
        // so there is zero timing dependency on inset callbacks.
        // ────────────────────────────────────────────────────────────────────────

        // Read status bar height synchronously – works on all API levels
        val statusBarResId = resources.getIdentifier("status_bar_height", "dimen", "android")
        val statusBarHeight = if (statusBarResId > 0)
            resources.getDimensionPixelSize(statusBarResId) else
            (24 * resources.displayMetrics.density + 0.5f).toInt()

        // Read navigation bar height synchronously
        val navBarResId = resources.getIdentifier("navigation_bar_height", "dimen", "android")
        val navBarHeight = if (navBarResId > 0)
            resources.getDimensionPixelSize(navBarResId) else 0

        // Container: dark background fills the gap behind status & nav bars
        val container = FrameLayout(this)
        container.setBackgroundColor(Color.parseColor("#090D16"))

        // Apply padding BEFORE setContentView so layout is correct on first pass
        container.setPadding(0, statusBarHeight, 0, navBarHeight)

        webView = WebView(this)
        webView.setBackgroundColor(Color.parseColor("#090D16"))
        webView.setLayerType(WebView.LAYER_TYPE_HARDWARE, null)

        val settings: WebSettings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        @Suppress("DEPRECATION")
        settings.databaseEnabled = true
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW

        webView.isClickable = true
        webView.isFocusable = true
        webView.isFocusableInTouchMode = true
        webView.requestFocus()
        webView.requestFocusFromTouch()
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        webView.addJavascriptInterface(AndroidBridge(), "AndroidBridge")
        webView.loadUrl("file:///android_asset/index.html")

        container.addView(
            webView,
            FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
            )
        )

        setContentView(container)

        // Secondary: also handle dynamic insets (display cutouts / foldables)
        // after the container is attached, so they override the initial padding
        // only when a more precise value is available.
        ViewCompat.setOnApplyWindowInsetsListener(container) { _, insets ->
            val bars = insets.getInsets(
                WindowInsetsCompat.Type.systemBars()
                        or WindowInsetsCompat.Type.displayCutout()
            )
            container.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            WindowInsetsCompat.CONSUMED
        }
        // Force inset dispatch now that the container is attached
        ViewCompat.requestApplyInsets(container)

        // Back navigation for internal SPA routing
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                webView.evaluateJavascript(
                    "window.handleAndroidBack ? window.handleAndroidBack() : false"
                ) { result ->
                    val handledByJs = result == "true" || result == "\"true\""
                    if (!handledByJs) {
                        if (webView.canGoBack()) {
                            webView.goBack()
                        } else {
                            isEnabled = false
                            onBackPressedDispatcher.onBackPressed()
                        }
                    }
                }
            }
        })
    }

    inner class AndroidBridge {
        @JavascriptInterface
        fun closeApp() {
            finish()
        }
    }
}
