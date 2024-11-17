import xor_cipher
import pytest

def test_guess_key_space_filter():
    # Create a sample encrypted message and key
    expected_message = ("Most secret operational order No. 3. In accordance with agreement with Japan, U-boat war is to be extended to include all enemy ships in the western Atlantic as far as 35 degrees West longitude, regardless of flag.")
    key = "xy"
    my_encrypt_message = xor_cipher.xor_encrypt(expected_message, key)

    #Positive tests:

    # Test with default parameters on a successful decrypt message
    my_est_spaces_th = round(0.7*(len(my_encrypt_message)/4.7-1))
    result = xor_cipher.guess_key_space_filter(my_encrypt_message, key_size = len(key), filter_result=True, spaces_th = my_est_spaces_th)
    assert len(result) == 1
    assert result[0][0] == key
    assert result[0][1] == expected_message

    #Test that ensure we are going over all results
    result = xor_cipher.guess_key_space_filter(my_encrypt_message, key_size = len(key), filter_result=False)
    assert len(result) ==  26 ** len(key)

    #Negative tests:

    # Test with different key sizes
    wrong_key_size = len(key) - 1
    result = xor_cipher.guess_key_space_filter(my_encrypt_message, wrong_key_size)
    assert len(result) == 0

    #Test low space th
    Low_space_th = 1
    result = xor_cipher.guess_key_space_filter(my_encrypt_message, key_size=len(key), filter_result=True,
                                               spaces_th=Low_space_th)
    assert len(result) > 1

    #Test high space th
    High_space_th = 1000
    result = xor_cipher.guess_key_space_filter(my_encrypt_message, key_size=len(key), filter_result=True,
                                               spaces_th=High_space_th)
    assert len(result) == 0

    #Invalid encrypted message
    # Test with None input
    None_enc_message = None
    with pytest.raises(Exception) as e:
        xor_cipher.guess_key_space_filter(None_enc_message, key_size=len(key), filter_result=True, spaces_th=my_est_spaces_th)
    assert "NoneType' object is not iterable" in str(e.value)

    #Invalid key size
    # Test key with negative value
    wrong_key_size = -1
    with pytest.raises(Exception) as e:
        xor_cipher.guess_key_space_filter(None, key_size= wrong_key_size, filter_result=True, spaces_th=my_est_spaces_th)
    assert "repeat argument cannot be negative" in str(e.value)