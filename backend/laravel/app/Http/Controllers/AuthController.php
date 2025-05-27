<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Http\Requests\LoginRequest;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

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

    /*
    public function addTable(Request $request)
    {
        Log::info('Adding table: '. $request);
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

        $user->update(['tables' => $updatedTablesString]);

        return response()->json(['message' => 'Table added successfully']);
    }
    */

    public function updateTable(Request $request)
    {
        Log::info('Updating tables: ' . $request);
        $this->purgeExpiredTokens();
        $user = $request->user();

        // Step 1: Parse the incoming request input
        $input = $request->input('table');
        $newTables = [];

        foreach (explode(';', $input) as $pair) {
            [$section, $charts] = explode(':', $pair) + [null, null];
            if ($section && $charts) {
                $newTables[$section] = array_map('trim', explode(',', $charts));
            }
        }

        // Step 2: Parse existing user table data
        $existingTables = [];
        $tablesString = $user->tables ?? '';
        if (!empty($tablesString)) {
            foreach (explode(';', $tablesString) as $pair) {
                [$section, $charts] = explode(':', $pair) + [null, null];
                if ($section && $charts) {
                    $existingTables[$section] = array_map('trim', explode(',', $charts));
                }
            }
        }

        // Step 3: Combine, add new charts, remove old ones
        $finalTables = [];

        foreach ($newTables as $section => $newCharts) {
            $existingCharts = $existingTables[$section] ?? [];
            // Keep only charts that are in the new request
            $filteredExisting = array_intersect($existingCharts, $newCharts);
            // Merge without duplication
            $merged = array_unique(array_merge($filteredExisting, $newCharts));
            sort($merged);
            $finalTables[$section] = $merged;
        }

        // Step 4: Rebuild the string to store in DB
        $updatedTablesString = implode(';', array_map(
            fn($section, $charts) => "$section:" . implode(',', $charts),
            array_keys($finalTables),
            $finalTables
        ));

        $user->update(['tables' => $updatedTablesString]);

        return response()->json(['message' => 'Tables updated successfully']);
    }
}
