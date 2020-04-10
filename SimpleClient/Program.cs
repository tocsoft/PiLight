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
        public static async Task Main()
        {
            var client = await Client.Discover();

            await client.TurnOnLight(Lights.Green, true);
            await Task.Delay(5000);
            await client.TurnOnLight(Lights.Amber, true);
            await Task.Delay(5000);
            await client.TurnOnLight(Lights.Red, true);
            await Task.Delay(5000);
        }
    }
}
