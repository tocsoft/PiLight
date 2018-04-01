using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PiLight.ClientController
{
    public static class Program
    {
        public static void Main()
        {
            var client = Client.Discover().GetAwaiter().GetResult();

            client.TurnOnLight(Lights.Green, true).GetAwaiter().GetResult(); ;
            Thread.Sleep(5000);
            client.TurnOnLight(Lights.Amber, true).GetAwaiter().GetResult(); ;
            Thread.Sleep(5000);
            client.TurnOnLight(Lights.Red, true).GetAwaiter().GetResult(); ;
            Thread.Sleep(5000);
        }
    }
}
