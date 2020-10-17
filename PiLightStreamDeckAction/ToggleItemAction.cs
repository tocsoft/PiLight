using PiLight.ClientController;
using StreamDeckLib;
using StreamDeckLib.Messages;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace OpenhabStreamDeckAction
{
    public enum LightState
    {
        None,
        Red,
        Amber,
        Green
    }

    [ActionUuid(Uuid = "tocsoft.streamdeck.pilight.switch")]
    public class ToggleItemAction : BaseStreamDeckActionWithSettingsModel<Models.PiLightOptions>
    {
        public LightState currentState;
        public bool paused = false;
        public bool loading = true;
        public string IPAddress { get; set; }


        public string context;
        private CancellationTokenSource cts;
        private Task t;
        private Client client;

        public ToggleItemAction()
        {
        }
        private void LoadStateBackground()
        {
            cts = new CancellationTokenSource();
            var token = cts.Token;
            t = Task.Run(async () =>
            {
                if (context != null)
                {
                    await Manager.SetImageAsync(context, $"images/allOffPaused@2x.png");
                }
                client = await Connect();

                while (!token.IsCancellationRequested)
                {
                    try
                    {
                        await LoadState();
                    }
                    catch (Exception ex)
                    {
                        if (context != null)
                        {
                            await Manager.SetImageAsync(context, $"images/allOffPaused@2x.png");
                        }
                    }
                    await Task.Delay(5000, token);
                }
            }, token);
        }
        private async Task LoadState()
        {
            client = client ?? await Connect();
            StatusInfo status;
            try
            {
                status = await client.GetStatus();
            }
            catch (Exception ex)
            {
                client = await Connect();
                status = await client.GetStatus();
            }

            paused = status.Pasued;

            if (status.Red)
            {
                currentState = LightState.Red;
            }
            else if (status.Amber)
            {
                currentState = LightState.Amber;
            }
            else if (status.Green)
            {
                currentState = LightState.Green;
            }
            else
            {
                currentState = LightState.None;
            }
            loading = false;
            await UpdateButtonState();
        }

        private async Task UpdateButtonState()
        {
            if (context != null)
            {
                var pausedString = "";
                if (paused) { pausedString = "Paused"; }

                switch (currentState)
                {
                    case LightState.None:
                        await Manager.SetImageAsync(context, $"images/allOff{pausedString}@2x.png");
                        break;
                    case LightState.Red:
                        await Manager.SetImageAsync(context, $"images/redOnly{pausedString}@2x.png");
                        break;
                    case LightState.Amber:
                        await Manager.SetImageAsync(context, $"images/amberOnly{pausedString}@2x.png");
                        break;
                    case LightState.Green:
                        await Manager.SetImageAsync(context, $"images/greenOnly{pausedString}@2x.png");
                        break;
                    default:
                        break;
                }
            }
        }

        public override async Task OnKeyUp(StreamDeckEventPayload args)
        {
            this.context = args.context;
            if (paused)
            {
                paused = false;
                client = client ?? await Connect();
                await client.Unpause();
            }
            else
            {
                paused = false;
                currentState++;
                currentState = (LightState)((int)currentState % 4);

                switch (currentState)
                {
                    case LightState.None:
                        await TurnOffAllLights();
                        break;
                    case LightState.Red:
                        await TurnOnLight(Lights.Red);
                        break;
                    case LightState.Amber:
                        await TurnOnLight(Lights.Amber);
                        break;
                    case LightState.Green:
                        await TurnOnLight(Lights.Green);
                        break;
                    default:
                        break;
                }
            }

            await UpdateButtonState();
        }

        private async Task TurnOffAllLights(int counter = 0)
        {
            try
            {
                client = client ?? await Connect();
                await client.TurnOffAllLights();
            }
            catch (Exception ex)
            {
                client = await Connect();
                await TurnOffAllLights(counter++);

                if (counter > 3)
                {
                    throw ex;
                }
            }
        }

        private async Task TurnOnLight(Lights light, int counter = 0)
        {
            try
            {
                client = client ?? await Connect();
                await client.TurnOnLight(light, false);
            }
            catch (Exception ex)
            {
                client = await Connect();
                await TurnOnLight(light, counter++);

                if (counter > 3)
                {
                    throw ex;
                }
            }
        }

        private async Task Unpause(int counter = 0)
        {
            try
            {
                client = client ?? await Connect();
                await client.Unpause();
            }
            catch (Exception ex)
            {
                client = await Connect();
                await Unpause(counter++);

                if (counter > 3)
                {
                    throw ex;
                }
            }
        }

        private Task<Client> Connect()
        {
            if (string.IsNullOrWhiteSpace(SettingsModel?.IPAddress))
            {
                return Client.Discover();
            }
            else
            {
                return Task.FromResult(new Client(new Uri("http://" + SettingsModel.IPAddress)));
            }
        }

        public override async Task OnDidReceiveSettings(StreamDeckEventPayload args)
        {
            await base.OnDidReceiveSettings(args); ;
            Restart();
        }

        public override async Task OnWillAppear(StreamDeckEventPayload args)
        {
            await base.OnWillAppear(args);
            this.context = args.context;
            Restart();
        }

        public override Task OnApplicationDidLaunch(StreamDeckEventPayload args)
        {
            return base.OnApplicationDidLaunch(args);
        }
        public override Task OnApplicationDidTerminate(StreamDeckEventPayload args)
        {
            return base.OnApplicationDidTerminate(args);
        }

        private async Task Restart()
        {
            client = null;
            this.cts?.Cancel();
            if (this.t != null)
            {
                await this.t;
            }
            LoadStateBackground();
        }

        public override async Task OnWillDisappear(StreamDeckEventPayload args)
        {
            this.cts.Cancel();
            await this.t;

            await base.OnWillDisappear(args);
        }
    }
}
