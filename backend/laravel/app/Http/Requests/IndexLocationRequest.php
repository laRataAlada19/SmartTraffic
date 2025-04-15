<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class IndexLocationRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }
    
    public function rules(): array
    {
        return [
            'location' => 'nullable|string|max:100',
            'direction' => 'nullable|string|max:50',
            'page' => 'nullable|integer|min:1',
            'per_page' => 'nullable|integer|min:1|max:100',
            'sort_by' => 'nullable|string|in:location,direction',
            'sort_order' => 'nullable|string|in:asc,desc',
        ];
    }
}
