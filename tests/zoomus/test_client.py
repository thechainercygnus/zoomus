import unittest

from zoomus import components, ZoomClient, util
from zoomus.client import API_BASE_URIS

try:
    from unittest import mock
except ImportError:
    import mock  # type: ignore


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ZoomClientTestCase))
    return suite


class ZoomClientTestCase(unittest.TestCase):
    def test_init_sets_config(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertEqual(
            client.config,
            {
                "api_key": "KEY",
                "api_secret": "SECRET",
                "data_type": "json",
                "token": util.generate_jwt("KEY", "SECRET"),
                "version": util.API_VERSION_2,
                "base_uri": API_BASE_URIS[util.API_VERSION_2],
            },
        )

    def test_invalid_api_version_raises_error(self):
        with self.assertRaisesRegexp(RuntimeError, "API version not supported: 42"):
            ZoomClient("KEY", "SECRET", version=42)

    def test_init_sets_config_with_timeout(self):
        client = ZoomClient("KEY", "SECRET", timeout=500)
        self.assertEqual(client.timeout, 500)

    def test_cannot_init_with_non_int_timeout(self):
        with self.assertRaises(ValueError) as context:
            ZoomClient("KEY", "SECRET", timeout="bad")
            self.assertEqual(
                context.exception.message, "timeout value must be an integer"
            )

    def test_init_creates_all_components(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertEqual(
            set(
                [
                    "contacts",
                    "group",
                    "live_stream",
                    "meeting",
                    "metric",
                    "past_meeting",
                    "phone",
                    "recording",
                    "report",
                    "room",
                    "user",
                    "webinar",
                ]
            ),
            set(client.components.keys()),
        )
        self.assertIsInstance(
            client.components["contacts"], components.contacts.ContactsComponentV2
        )
        self.assertIsInstance(
            client.components["meeting"], components.meeting.MeetingComponentV2
        )
        self.assertIsInstance(
            client.components["metric"], components.metric.MetricComponentV2
        )
        self.assertIsInstance(
            client.components["past_meeting"],
            components.past_meeting.PastMeetingComponentV2,
        )
        self.assertIsInstance(
            client.components["report"], components.report.ReportComponentV2
        )
        self.assertIsInstance(
            client.components["user"], components.user.UserComponentV2
        )
        self.assertIsInstance(
            client.components["webinar"], components.webinar.WebinarComponentV2
        )
        self.assertIsInstance(
            client.components["recording"], components.recording.RecordingComponentV2
        )
        self.assertIsInstance(
            client.components["phone"], components.phone.PhoneComponentV2
        )
        self.assertIsInstance(
            client.components["group"], components.group.GroupComponentV2
        )
        self.assertIsInstance(
            client.components["live_stream"],
            components.live_stream.LiveStreamComponentV2,
        )
        self.assertIsInstance(
            client.components["room"], components.room.RoomComponentV2
        )

    def test_api_version_defaults_to_2(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_VERSION_2]
            )

    def test_can_set_api_version_to_1(self):
        client = ZoomClient("KEY", "SECRET", version=util.API_VERSION_1)
        self.assertEqual(client.config["version"], util.API_VERSION_1)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_VERSION_1]
            )

    def test_can_set_base_uri_to_gdpr(self):
        client = ZoomClient("KEY", "SECRET", base_uri=API_BASE_URIS[util.API_GDPR])
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_GDPR]
            )

    def test_can_set_custom_base_uri(self):
        client = ZoomClient(
            "KEY", "SECRET", version=util.API_VERSION_1, base_uri="https://www.test.com"
        )
        self.assertEqual(client.config["version"], util.API_VERSION_1)
        for key in client.components.keys():
            self.assertEqual(client.components[key].base_uri, "https://www.test.com")

    def test_can_set_api_version_to_1_and_set_custom_base_uri(self):
        client = ZoomClient("KEY", "SECRET", base_uri=API_BASE_URIS[util.API_GDPR])
        self.assertEqual(client.config["version"], util.API_VERSION_2)
        for key in client.components.keys():
            self.assertEqual(
                client.components[key].base_uri, API_BASE_URIS[util.API_GDPR]
            )

    def test_can_get_api_key(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertEqual(client.api_key, "KEY")

    def test_can_set_api_key(self):
        client = ZoomClient("KEY", "SECRET")
        client.api_key = "NEW-KEY"
        self.assertEqual(client.api_key, "NEW-KEY")

    def test_can_get_api_secret(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertEqual(client.api_secret, "SECRET")

    def test_can_set_api_secret(self):
        client = ZoomClient("KEY", "SECRET")
        client.api_secret = "NEW-SECRET"
        self.assertEqual(client.api_secret, "NEW-SECRET")

    def test_can_get_contacts_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.contacts, components.contacts.ContactsComponentV2)

    def test_can_get_meeting_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.meeting, components.meeting.MeetingComponentV2)

    def test_can_get_report_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.report, components.report.ReportComponentV2)

    def test_can_get_user_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.user, components.user.UserComponentV2)

    def test_can_get_webinar_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.webinar, components.webinar.WebinarComponentV2)

    def test_can_get_recording_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(
            client.recording, components.recording.RecordingComponentV2
        )

    def test_can_get_live_stream_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(
            client.live_stream, components.live_stream.LiveStreamComponentV2
        )

    def test_can_get_phone_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.phone, components.phone.PhoneComponentV2)

    def test_can_get_group_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.group, components.group.GroupComponentV2)

    def test_can_get_room_component(self):
        client = ZoomClient("KEY", "SECRET")
        self.assertIsInstance(client.room, components.room.RoomComponentV2)

    def test_can_use_client_with_context(self):
        with ZoomClient("KEY", "SECRET") as client:
            self.assertIsInstance(client, ZoomClient)

    @mock.patch("zoomus.client.util.generate_jwt")
    def test_refresh_token_replaces_config_token_with_new_jwt(self, mock_jwt):
        client = ZoomClient("KEY", "SECRET")
        client.refresh_token()
        mock_jwt.assert_called_with("KEY", "SECRET")
        self.assertEqual(client.config["token"], (mock_jwt.return_value,))


if __name__ == "__main__":
    unittest.main()
