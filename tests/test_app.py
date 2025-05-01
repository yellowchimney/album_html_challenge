from playwright.sync_api import Page, expect

# Tests for success scenario:

def test_get_album_by_id_returns_for_valid_id(page, test_web_address):
    page.goto(f"http://{test_web_address}/albums/12")
    header_tag = page.locator("h1")
    title = page.locator(".t-title")
    year = page.locator(".t-release-year")
    name = page.locator(".t-artist-name")

    expect(header_tag).to_have_text("Album")
    expect(title).to_contain_text("Title: Ring Ring")
    expect(year).to_have_text("Release year: 1973")
    expect(name).to_have_text("Artist: ABBA")

# Test for invalid ID:

def test_get_album_by_id_returns_error_page_for_invalid_id(page, test_web_address):
    page.goto(f"http://{test_web_address}/albums/999")
    header_tag = page.locator("h1")
    error_message = page.locator(".t-error-message")

    expect(header_tag).to_have_text("Error")
    expect(error_message).to_have_text("No album found with the given ID.")

