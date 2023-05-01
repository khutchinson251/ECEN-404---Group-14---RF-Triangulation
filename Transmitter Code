#include <msp430g2553.h>
#define TXD BIT2
#define RXD BIT1

void String_TX(char * data);
int main(void)
{
   WDTCTL = WDTPW + WDTHOLD;                // Stop WDT
   DCOCTL = 0;                              // Select lowest DCOx and MODx settings
   BCSCTL1 = CALBC1_1MHZ;                   // Set DCO
   DCOCTL = CALDCO_1MHZ;
   P1SEL |= RXD + TXD ;                     // P1.1 = RXD, P1.2=TXD
   P1SEL2 |= RXD + TXD ;                    // P1.1 = RXD, P1.2=TXD
   UCA0CTL1 |= UCSSEL_2;                    // SMCLK
   UCA0BR0 = 0x68;                          // 1MHz 9600, 104 in dec
   UCA0BR1 = 0x00;                          // 1MHz 9600
   UCA0MCTL = UCBRS0;                       // Modulation UCBRSx = 1
   UCA0CTL1 &= ~UCSWRST;                    // **Initialize USCI state machine**
   ///Start looping///
   while(1)
   {
           String_TX("30.623230, -96.333884\r");        //GPS message here
           __delay_cycles(1000);        //Wait
   }
 }

void String_TX(char * data)                 // String function
   {
       unsigned int i=0;
       while(data[i])                       // Increment through array, look for null pointer (0) at end of string
       {
           while (!(IFG2&UCA0TXIFG));     // Wait for TX/RX bus to clear
           UCA0TXBUF = data[i];             // Send out element i of data array to UART bus
           i++; // Increment variable for array address
       }
   }



