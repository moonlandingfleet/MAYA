package com.mayaboss.android

import android.app.Dialog
import android.graphics.Bitmap
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.ui.platform.ComposeView
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.zxing.BarcodeFormat
import com.google.zxing.MultiFormatWriter
import com.google.zxing.common.BitMatrix
import com.journeyapps.barcodescanner.BarcodeEncoder
import com.mayaboss.android.network.MAYAApiService
import com.mayaboss.android.ui.MainScreen
import com.mayaboss.android.viewmodel.MAYAViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

data class Offer(
    val id: String,
    val satsExpected: Long,
    val risk: String,
    val merchantBlurb: String
)

interface OfferApiService {
    @GET("offer")
    fun getOffers(): Call<List<Offer>>
    
    companion object {
        private const val BASE_URL = "https://api.example.com/"
        
        fun create(): OfferApiService {
            val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
            return retrofit.create(OfferApiService::class.java)
        }
    }
}

class MainActivity : AppCompatActivity() {
    
    private lateinit var showQRButton: Button
    private lateinit var refreshOffersButton: Button
    private lateinit var offersRecyclerView: RecyclerView
    private lateinit var offerAdapter: OfferAdapter
    
    // Static test invoice for Brick 2
    private val testLightningInvoice = "lntb210n1pj4t64dpp58zj20fp6yzpw866066zp3gktq5393sw675w06hf555g8vaky3nqsdq5g9kxy7fqd9h8vmmfvdjjqen0wgsrzgrsd9ux2mrnypshggr5xscqzpgxqrrsssp596855hx006m75ek5407yc0k48d8jzmmg8tsk6f23vsaal5jzq9qyyssq658787j5yc8s3q90y7dxes0tjy34404428g5m90xzfslm90jk5n00sx00dfs8jge857clg46a0jag4567snh4dsj8k95cqhlvaj"
    
    private val offers = mutableListOf<Offer>()
    private lateinit var offerApiService: OfferApiService
    
    private val handler = Handler(Looper.getMainLooper())
    private val paymentCheckRunnable = object : Runnable {
        override fun run() {
            // Simulate checking for payments
            checkForPayments()
            // Schedule the next check in 30 seconds
            handler.postDelayed(this, 30000)
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Initialize the API service
        offerApiService = OfferApiService.create()
        
        initViews()
        setupRecyclerView()
        setupClickListeners()
        
        // Load initial offers
        loadOffers()
        
        // Start checking for payments
        startPaymentChecking()
        
        // Add Compose UI
        val composeView = ComposeView(this)
        composeView.setContent {
            MaterialTheme {
                Surface {
                    val apiService = MAYAApiService.create("http://localhost:8080/") // Adjust base URL as needed
                    val viewModel = ViewModelProvider(this, MAYAViewModelFactory(apiService))[MAYAViewModel::class.java]
                    MainScreen(viewModel)
                }
            }
        }
        // Add composeView to your layout as needed
        // For now, we'll add it to the main layout
        val mainLayout = findViewById<androidx.constraintlayout.widget.ConstraintLayout>(R.id.mainLayout)
        composeView.layoutParams = androidx.constraintlayout.widget.ConstraintLayout.LayoutParams(
            androidx.constraintlayout.widget.ConstraintLayout.LayoutParams.MATCH_PARENT,
            600 // Set height as needed
        )
        mainLayout.addView(composeView)
    }
    
    
    override fun onDestroy() {
        super.onDestroy()
        // Stop checking for payments when the activity is destroyed
        handler.removeCallbacks(paymentCheckRunnable)
    }
    
    private fun initViews() {
        showQRButton = findViewById(R.id.showQRButton)
        refreshOffersButton = findViewById(R.id.refreshOffersButton)
        offersRecyclerView = findViewById(R.id.offersRecyclerView)
    }
    
    private fun setupRecyclerView() {
        offerAdapter = OfferAdapter(offers) { offer ->
            showPaymentQR(offer)
        }
        offersRecyclerView.layoutManager = LinearLayoutManager(this)
        offersRecyclerView.adapter = offerAdapter
    }
    
    private fun setupClickListeners() {
        showQRButton.setOnClickListener {
            showStaticQR()
        }
        
        refreshOffersButton.setOnClickListener {
            loadOffers()
        }
    }
    
    private fun showStaticQR() {
        showQRDialog(testLightningInvoice)
    }
    
    private fun showPaymentQR(offer: Offer) {
        // For now, we'll use the static invoice
        // In a real implementation, this would be a dynamic invoice for the specific offer
        showQRDialog(testLightningInvoice)
    }
    
    private fun showQRDialog(invoice: String) {
        val dialog = Dialog(this)
        dialog.setContentView(R.layout.qr_dialog)
        
        val qrCodeImageView = dialog.findViewById<ImageView>(R.id.qrCodeImageView)
        val invoiceTextView = dialog.findViewById<TextView>(R.id.invoiceTextView)
        val closeButton = dialog.findViewById<Button>(R.id.closeButton)
        
        try {
            val bitmap = generateQRCode(invoice)
            qrCodeImageView.setImageBitmap(bitmap)
        } catch (e: Exception) {
            Toast.makeText(this, "Error generating QR code", Toast.LENGTH_SHORT).show()
        }
        
        invoiceTextView.text = invoice
        
        closeButton.setOnClickListener {
            dialog.dismiss()
        }
        
        dialog.show()
    }
    
    private fun generateQRCode(content: String): Bitmap {
        val multiFormatWriter = MultiFormatWriter()
        val bitMatrix: BitMatrix = multiFormatWriter.encode(content, BarcodeFormat.QR_CODE, 400, 400)
        val barcodeEncoder = BarcodeEncoder()
        return barcodeEncoder.createBitmap(bitMatrix)
    }
    
    private fun loadOffers() {
        offerApiService.getOffers().enqueue(object : Callback<List<Offer>> {
            override fun onResponse(call: Call<List<Offer>>, response: Response<List<Offer>>) {
                if (response.isSuccessful) {
                    response.body()?.let { offerList ->
                        offers.clear()
                        offers.addAll(offerList)
                        offerAdapter.notifyDataSetChanged()
                        Toast.makeText(this@MainActivity, "Offers loaded", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    // Use mock data if API call fails
                    loadMockOffers()
                }
            }
            
            override fun onFailure(call: Call<List<Offer>>, t: Throwable) {
                // Use mock data if network call fails
                loadMockOffers()
                Toast.makeText(this@MainActivity, "Network error, using mock data", Toast.LENGTH_SHORT).show()
            }
        })
    }
    
    private fun loadMockOffers() {
        offers.clear()
        offers.add(Offer("1", 2100, "Low", "Coffee Shop - 2% discount"))
        offers.add(Offer("2", 5000, "Medium", "Uber Ride - 3% discount"))
        offers.add(Offer("3", 15000, "High", "Airline Ticket - 5% discount"))
        offerAdapter.notifyDataSetChanged()
    }
    
    private fun startPaymentChecking() {
        handler.post(paymentCheckRunnable)
    }
    
    private fun checkForPayments() {
        // In a real implementation, this would check with a Lightning node
        // or payment processor to see if any payments have been received
        // For now, we'll just show a toast occasionally to simulate this
        if (Math.random() > 0.7) { // 30% chance to show a payment notification
            runOnUiThread {
                Toast.makeText(this, R.string.payment_received, Toast.LENGTH_SHORT).show()
            }
        }
    }
}

class OfferAdapter(
    private val offers: List<Offer>,
    private val onItemClick: (Offer) -> Unit
) : RecyclerView.Adapter<OfferAdapter.OfferViewHolder>() {
    
    class OfferViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val merchantBlurbTextView: TextView = view.findViewById(R.id.merchantBlurbTextView)
        val satsExpectedTextView: TextView = view.findViewById(R.id.satsExpectedTextView)
        val riskTextView: TextView = view.findViewById(R.id.riskTextView)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): OfferViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.offer_item, parent, false)
        return OfferViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: OfferViewHolder, position: Int) {
        val offer = offers[position]
        holder.merchantBlurbTextView.text = offer.merchantBlurb
        holder.satsExpectedTextView.text = "${offer.satsExpected} sats"
        holder.riskTextView.text = "Risk: ${offer.risk}"
        
        holder.itemView.setOnClickListener {
            onItemClick(offer)
        }
    }
    
    override fun getItemCount() = offers.size
}

class MAYAViewModelFactory(private val apiService: MAYAApiService) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(MAYAViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return MAYAViewModel(apiService) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}