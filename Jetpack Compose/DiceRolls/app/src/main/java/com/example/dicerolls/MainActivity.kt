package com.example.dicerolls

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.requiredHeight
import androidx.compose.foundation.layout.requiredWidth
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.view.WindowCompat
import com.google.accompanist.systemuicontroller.rememberSystemUiController
import androidx.compose.ui.graphics.Color
import com.example.dicerolls.ui.theme.DiceRollsTheme


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        setContent {
            DiceRollsTheme {
                // A surface container using the 'background' color from the theme
                val systemUiController = rememberSystemUiController()
                SideEffect {
                    systemUiController.setStatusBarColor(
                        color = Color.White,
                        darkIcons = false
                    )
                }
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    OutputNumber()

                }
            }
        }
    }
}



@Composable
fun OutputNumber() {
    val numbers = listOf(1, 2, 3, 4, 5, 6)
    var roll1  by remember{ mutableStateOf(numbers.random())}
    var roll2  by remember{ mutableStateOf(numbers.random())}
    Column(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.statusBars),

        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Your rolled numbers are:" +
                    "\n${roll1.toString()} & ${roll2.toString()}" +
                    "\nGiving a total of:" +
                    "\n${(roll1+roll2).toString()}" +
                    "\n",
            fontSize = 20.sp,
            textAlign = TextAlign.Center
        )
        Button(
            shape = CircleShape,
            modifier = Modifier
                .requiredHeight(100.dp)
                .requiredWidth(100.dp),
            onClick = {
                roll1 = numbers.random()
                roll2 = numbers.random()
            }) {
            Text(
                "Click"
            )
        }
    }
}



@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    DiceRollsTheme {

    }
}