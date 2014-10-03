

import testLib

class TestAddLoginUser(testLib.RestTestCase):

    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAddLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : '1'} )
        self.assertResponse(respData, count = 1, errCode = self.SUCCESS)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : '2'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_CREDENTIALS)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : '1'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : '1'} )
        self.assertResponse(respData, count = 3)
   
    def testAddMultiple(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : '1'} )
        self.assertResponse(respData, count = 1, errCode = self.SUCCESS)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : '2'} )
        self.assertResponse(respData, count = 1, errCode = self.SUCCESS)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : '1'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : '2'} )
        self.assertResponse(respData, count = 2)
        
    def testAddDuplicate(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'asd'} )
        self.assertResponse(respData, count = 1, errCode = self.SUCCESS)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'asd'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_USER_EXISTS)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'asd'} )
        self.assertResponse(respData, count = 2, errCode = self.SUCCESS)
        
    def testAddBlankUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_USERNAME)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_CREDENTIALS)
        
    def testAddLongUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'abcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyz', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_USERNAME)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'abcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyz', 'password' : 'password'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_CREDENTIALS)
        
    def testAddLongPassword(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'abcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyz'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_PASSWORD) 
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'abcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyz'} )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_CREDENTIALS)
           
    def testAddNoUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'password' : '' } )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_USERNAME)
        
    def testAddNoPassword(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1' } )
        self.assertResponse(respData, count = None, errCode = self.ERR_BAD_PASSWORD)

# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()