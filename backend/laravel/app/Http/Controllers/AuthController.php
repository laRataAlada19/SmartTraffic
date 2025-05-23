<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\LoginRequest;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use App\Models\User;
use Illuminate\Http\Request;

class AuthController extends Controller
{ 
    private function purgeExpiredTokens()
    {
        // Only deletes if token expired 2 hours ago
        $dateTimetoPurge = now()->subHours(2);
        DB::table('personal_access_tokens')
            ->where('expires_at', '<', $dateTimetoPurge)->delete();
    }

    private function revokeCurrentToken(User $user)
    {
        $currentTokenId = $user->currentAccessToken()->id;
        $user->tokens()->where('id', $currentTokenId)->delete();
    }

    public function login(LoginRequest $request)
    {
        $this->purgeExpiredTokens();
        $credentials = $request->validated();
        if (!Auth::attempt($credentials)) {
            return response()->json(['message' => 'Unauthorized'], 401);
        }
        $token = $request->user()->createToken(
            'authToken',
            ['*'],
            now()->addHours(2)
        )->plainTextToken;
        return response()->json(['token' => $token]);
    }

    public function logout(Request $request)
    {
        $this->purgeExpiredTokens();
        $this->revokeCurrentToken($request->user());
        return response()->json(null, 204);
    }

    public function refreshToken(Request $request)
    {
        // Revokes current token and creates a new token
        $this->purgeExpiredTokens();
        $this->revokeCurrentToken($request->user());
        $token = $request->user()->createToken(
            'authToken',
            ['*'],
            now()->addHours(2)
        )->plainTextToken;
        return response()->json(['token' => $token]);
    }
    public function getUserTables(Request $request)
    {
        $this->purgeExpiredTokens();
        $user = $request->user();

        $tables = DB::table('users')
            ->where('id', $user->id)
            ->value('tables'); 

        return response()->json(['tables' => $tables]);
    }
    public function addTable(Request $request)
    {
        $this->purgeExpiredTokens();
        $user = $request->user();
    

        $newTable = $request->input('table'); 
        $tablesString = $user->tables ?? '';
        $tablesArray = [];
        if (!empty($tablesString)) {
            $pairs = explode(';', $tablesString);
            foreach ($pairs as $pair) {
                [$key, $value] = explode(':', $pair) + [null, null];
                if ($key !== null && $value !== null) {
                    $tablesArray[$key] = $value;
                }
            }
        }

        [$newKey, $newValue] = explode(':', $newTable) + [null, null];
        if ($newKey !== null && $newValue !== null) {
            $tablesArray[$newKey] = $newValue;
        }
    
        $updatedTablesString = implode(';', array_map(
            fn($key, $value) => "$key:$value",
            array_keys($tablesArray),
            $tablesArray
        ));

        DB::table('users')
            ->where('id', $user->id)
            ->update(['tables' => $updatedTablesString]);
    
        return response()->json(['message' => 'Table added successfully']);
    }
}