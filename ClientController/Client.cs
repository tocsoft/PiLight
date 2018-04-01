using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace PiLight.ClientController
{
    public class Client
    {
        private HttpClient httpClient;

        public Client(Uri uri)
        {
            this.httpClient = new HttpClient()
            {
                BaseAddress = uri
            };
        }

        public static async Task<Client> Discover(TimeSpan? timeout = null)
        {
            timeout = timeout ?? TimeSpan.FromSeconds(30);

            UdpClient client = new UdpClient();

            client.ExclusiveAddressUse = false;
            IPEndPoint localEp = new IPEndPoint(IPAddress.Any, 1234);

            client.Client.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            client.ExclusiveAddressUse = false;

            client.Client.Bind(localEp);

            IPAddress multicastaddress = IPAddress.Parse("239.255.4.3");
            client.JoinMulticastGroup(multicastaddress);

            client.Client.ReceiveTimeout = (int)timeout.Value.TotalMilliseconds;
            try
            {
                var result = await client.ReceiveAsync();

                string strData = Encoding.Unicode.GetString(result.Buffer);
                // strData == ip addres

                return new Client(new Uri("http://" + strData));
            }
            catch (SocketException ex) when (ex.SocketErrorCode == SocketError.TimedOut)
            {
                return null;
            }
        }

        public Task TurnOnLight(Lights light, bool flash = false)
        {
            var action = flash ? "flash" : "light";
            return this.httpClient.GetAsync($"/{action}/{light.ToString().ToLower()}");
        }
    }
    public enum Lights
    {
        Red,
        Amber,
        Green
    }
}
