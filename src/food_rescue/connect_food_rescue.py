import json
import ssl
import paho.mqtt.client as mqtt

from get_food_rescue_conf import get_food_rescue_for_all_locations

MQTT_BROKER = "consumermqtt.zomato.com"
MQTT_PORT = 443


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to Zomato Food Rescue")
        for topic in userdata.get("topics", []):
            client.subscribe(topic, qos=1)
            print(f"Subscribed to: {topic}")
    else:
        print(f"❌ Connection failed with code: {rc}")


def on_message(client, userdata, msg):
    """Callback when a message is received."""
    print("\n" + "=" * 60)
    print(f"🔔 FOOD RESCUE ALERT!")
    print(f"Topic: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Data: {json.dumps(payload, indent=2)}")
    except:
        print(f"Raw: {msg.payload.decode()}")
    print("=" * 60 + "\n")


def on_disconnect(client, userdata, disconnect_flags, rc, properties=None):
    """Callback when disconnected."""
    print(f"⚠️ Disconnected from MQTT broker (code: {rc})")


def main():
    # Get food rescue config for all locations
    print("Fetching food rescue configuration...")
    results = get_food_rescue_for_all_locations()
    
    if not results:
        print("No food rescue channels found")
        return
    
    # Collect all unique topics and get MQTT credentials
    topics = set()
    mqtt_username = None
    mqtt_password = None
    mqtt_keepalive = 900
    
    for result in results:
        for channel in result["food_rescue_channels"]:
            if channel["channel_name"]:
                topics.add(channel["channel_name"])
            if not mqtt_username:
                mqtt_username = channel["mqtt_username"]
                mqtt_password = channel["mqtt_password"]
                mqtt_keepalive = channel["mqtt_keepalive"] or 900
    
    print(f"\nFound {len(topics)} unique food rescue topics:")
    for topic in topics:
        print(f"  - {topic}")
    
    print(f"\nMQTT Credentials:")
    print(f"  Username: {mqtt_username}")
    print(f"  Password: {mqtt_password}")
    print(f"  Keepalive: {mqtt_keepalive}s")
    
    # Create MQTT client (TCP with TLS, not websockets)
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="zomato_food_rescue_client",
        transport="tcp",
        userdata={"topics": list(topics)}
    )
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Set credentials
    client.username_pw_set(mqtt_username, mqtt_password)
    
    # Configure TLS
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    
    # Connect
    print(f"\nConnecting to {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=mqtt_keepalive)
        print("Waiting for food rescue notifications... (Ctrl+C to stop)")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\nStopping...")
        client.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
